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

def home(request):
	return redirect('results')


def results(request):
	data = get_tournament()
	table = tabulate(data, tablefmt='html')
	return render(request, 'strategy/results.html', {'table': table})

def upload(request):
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			strat = Strategy(main=request.FILES['main'], user=request.user)
			strat.save()
			filename = strategy_by_user(request.user)
			print("COMPILE", filename)
			flag = compil(filename, "compiled_" + filename.split('.')[0])
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