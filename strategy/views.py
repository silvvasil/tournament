from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import UploadForm
from .models import Strategy
from django.contrib.auth.models import User
from .tournament import compil, get_tournament, strategy_by_user
from tabulate import tabulate
import streamlit as st
from bs4 import BeautifulSoup as bs


def home(request):
    return redirect('results')


def battle(request, first, second):
    users = User.objects.all()
    strategy_1 = strategy_by_user(users[first]).split('/')[1]
    strategy_2 = strategy_by_user(users[second]).split('/')[1]
    print("Battle", strategy_1, strategy_2)
    return render(request, 'strategy/visualizer.html',
                  {'battle': f'battlelogs/battlelog_{strategy_1}_{strategy_2}.js'})


def render_html_by_table(data):
    print(data)
    for i in range(1, len(data)):
        print(data[i])
        ind = data[i][0]
        for j in range(2, len(data[i]) - 1):
            data[i][j] = f"<a href=battle/{ind}/{data[0][j]}>{data[i][j]}</a>"
    table = tabulate(data, tablefmt='html')
    soup = bs(table)
    table = table.replace("&gt;", ">").replace("&lt;", "<")
    print(soup.prettify())

    return table


def results(request):
    data = get_tournament()
    return render(request, 'strategy/results.html', {'table': render_html_by_table(data)})


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            strat = Strategy(main=request.FILES['main'], user=request.user)
            strat.save()
            filename = strategy_by_user(request.user)
            print("COMPILE", filename)
            flag = compil(filename, "compiled_" + filename)
            if flag:
                messages.success(request, ("Submitted"))
            else:
                messages.error(request, ("Submission Failed"))
            return redirect('results')
        else:
            context = {'form': UploadForm}
            return render(request, 'strategy/index.html', context)
    context = {'form': UploadForm}
    return render(request, 'strategy/index.html', context)
