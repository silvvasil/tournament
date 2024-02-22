from django.contrib.auth.models import User
from .models import Strategy
import os
import json
from functools import lru_cache
import threading
import json

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def strategy_by_user(user):
    try:
        st = Strategy.objects.filter(user=user)
        return st[len(st) - 1].main.name
    except ValueError: 
        return "strategies/no_strategy.cpp"

def all_users():
    return User.objects.all()


def users_list():
    users = User.objects.all()
    return [user.username.split('-')[-1] for user in users]


def replace_bitsstdcpph(filename):
    try:
        f = open(filename, 'r')
        lines = f.read()
        # print(lines)
        f.close()
        lines = lines.replace("#include <bits/stdc++.h>", "#include <iostream>\n#include <iomanip>\n#include <vector>\n#include <cmath>\n#include <algorithm>\n#include <string>\n#include <deque>\n#include <functional>\n#include <set>\n#include <map>\n#include <random>\n#include <memory>\n#include <cassert>\n#include <fstream>\n#include <unordered_map>\n#include <unordered_set>\n#include <bitset>\n#include <time.h>\n#include <stack>\n#include <queue>\n#include <complex>\n#include <chrono>\n")
        f = open(filename, 'w')
        f.write(lines)
        f.close()
    except:
        f.close()
        pass
    

def compil(filename, filename_out):
    replace_bitsstdcpph(filename)
    res = os.system(f"g++ {filename} -O3 -o {filename_out} -std=c++17")
    print(res)
    if res:
        os.system(f"cp compiled_strategies/no_strategy {filename_out}")
        return False
    return True


@lru_cache
def versus(filename1, filename2, count=2):
    ans = [0, 0]
    for ind in range(count):
        os.system(f"python3 interactor.py {filename1} {filename2}")
        file = open("./visualizer/battlelog.js", "r").read()
        obj = file[file.find("{"): file.rfind("}") + 1]
        h = json.loads(obj.replace("'", '"'))
        if ind % 2 == 0:
            ans[h["winner"] - 1] += 1
        else:
            ans[2 - h["winner"]] += 1
        filename1, filename2 = filename2, filename1
    
    if ans[0] == ans[1]:
        return 0.5
    return 1 - ans.index(max(ans))


def get_tournament(cnt_threads=5):
    threads = []
    players = all_users()
    # print('\n'.join(users_list()))
    strats = ["compiled_" + strategy_by_user(user).split('.')[0] for user in players]
    # print('\n'.join(strats))
    n = len(players)
    table = [[0] * n for _ in range(n)]
    for i in range(n):
        print("Testing ", strats[i])
        for j in range(i + 1, n):
            threads.append(ThreadWithResult(target=versus, args=(strats[i], strats[j], 2,)))
            threads[-1].start()
            threads[-1].join()
            # table[i][j] = result
            # table[j][i] = 1 - result

    # for thread in threads:
        # thread.join(2)
    id = 0
    for i in range(n):
        for j in range(i + 1, n):
            table[i][j] = threads[id].result
            table[j][i] = 1 - threads[id].result
            id += 1
    users = [""] * 2 + [str(i) + "  "  for i in range(len(table))] + ["sum"]
    return [users] + sorted([[i] + [users_list()[i]] + table[i] + [sum(table[i])] for i in range(len(table))], key=lambda x: x[-1], reverse=True)



# print(get_tournament("strategies"))
# versus(compil("vasya_nextcol.cpp", "first"), compil("vasya_nextcol.cpp", "second"))