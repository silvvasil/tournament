#!/usr/bin/env python3

from subprocess import Popen, PIPE
from copy import deepcopy
from random import randint
from threading import Timer
import sys

sys.setrecursionlimit(10**6)

PREFIX = './'

class Solution:
    def __init__(self, cmd, timeout=2):
        self.cmd = PREFIX + cmd
        self.timeout = timeout
    def interact(self, inp):
        p = Popen([self.cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        def kill_proc(p):
            p.kill()
            kill_proc.overtime = True
        kill_proc.overtime = False
        timer = Timer(self.timeout, kill_proc, [p])
        timer.start()
        try:
            stdout, stderr = p.communicate(inp.encode())
        except:
            print('except')
            if kill_proc.overtime:
                return "TL"
            return "RE"
        timer.cancel()
        if kill_proc.overtime:
            return "TL"
        if p.returncode != 0:
            return "RE"
        return stdout, stderr

class FilyaSolution:
    def __init__(self, cmd, timeout=2):
        self.sol = Solution(cmd, timeout)
    def interact(self, field):
        inp = '\n'.join(''.join(map(str, s)) for s in field)+'\n'
        res = self.sol.interact(inp)
        if res == "RE":
            return "RE", 0
        if res == "TL":
            return "TL", 0
        try:
            ans = int(res[0].strip())
        except:
            return "PE", res[0].decode()
        if ans < 1 or ans > 6:
            return "PE", res[0].decode()
        if ans == field[0][0] or ans == field[-1][-1]:
            return "PE", res[0].decode()
        return "OK", ans

class Filya:
    def __init__(self, player1, player2):
        self.player1 = FilyaSolution(player1)
        self.player2 = FilyaSolution(player2)
        self.field = [[0]*45 for i in range(41)]
        self.gen()
        self.startfield = deepcopy(self.field)
        self.log = []
        self.current = 1
        self.used = [[False]*45 for i in range(41)]
        self.startscore = self.score()
    def gen(self):
        self.field = [[randint(1, 6) for y in range(45)] for x in range(41)]
        if self.field[-1][-1] == self.field[0][0]:
            self.field[-1][-1] = self.field[-1][-1] % 6 + 1
    def make_move(self, player, move):
        if player == 1:
            self._make_move((0, 0), move, self.field[0][0])
        else:
            self._make_move((40, 44), move, self.field[40][44])
    def _make_move(self, cell, move, old):
        if self.field[cell[0]][cell[1]] != old:
            return
        self.field[cell[0]][cell[1]] = move
        dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for dx, dy in dirs:
            x, y = cell[0] + dx, cell[1] + dy
            if (x >= 0) and (y >= 0) and (x < 41) and (y < 45):
                self._make_move((x, y), move, old)
    def getfield(self, player):
        if player == 1:
            return deepcopy(self.field)
        elif player == 2:
            return [[y for y in reversed(x)] for x in reversed(self.field)]
        else:
            raise Exception("Wrong player")
    def proceed(self):
        # print('\n'.join(''.join(map(str, s)) for s in self.field)+'\n', file=sys.stderr)
        if self.current == 1:
            status, move = self.player1.interact(self.getfield(self.current))
        else:
            status, move = self.player2.interact(self.getfield(self.current))
        self.log.append([status, move])
        # print("Player %d: %s [%s]" % (self.current, str(move), status), file = sys.stderr)
        if status != 'OK':
            return False, status
        self.make_move(self.current, move)
        self.current = 3 - self.current
        return True, 'OK'
    def score(self):
        self.used = [[False]*45 for i in range(41)]
        return [self._score((0, 0), self.field[0][0]), self._score((40, 44), self.field[40][44])]
    def _score(self, cell, old):
        if self.used[cell[0]][cell[1]]:
            return 0
        if self.field[cell[0]][cell[1]] != old:
            return 0
        self.used[cell[0]][cell[1]] = True
        ans = 1
        dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for dx, dy in dirs:
            x, y = cell[0] + dx, cell[1] + dy
            if (x >= 0) and (y >= 0) and (x < 41) and (y < 45):
                ans += self._score((x, y), old)
        return ans
    def run(self):
        oldscore = self.score()
        oldscorecnt = 0
        while True:
            cont, status = self.proceed()
            score = self.score()
            self.log[-1].append(score)
            if not cont:
                break
            if score == oldscore:
                oldscorecnt += 1
            else:
                oldscore = score
                oldscorecnt = 0
            if oldscorecnt == 10:
                break
        res = {
            'winner': 1 if oldscore[0] > oldscore[1] else 2,
            'log': self.log,
            'field': self.startfield,
            'startscore': self.startscore,
            'players': [self.player1.sol.cmd[len(PREFIX):], self.player2.sol.cmd[len(PREFIX):]]
        }
        if status != 'OK':
            res['winner'] = 3 - self.current
        return res


pl1, pl2 = sys.argv[1:3]
F = Filya(pl1, pl2)
#print('\n'.join(' '.join(map(str, s)) for s in F.field)+'\n', file=sys.stderr)

js = F.run()
with open('visualizer/battlelog.js', 'w') as log:
    print('game =', js, file=log)
