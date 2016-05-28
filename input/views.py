from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import User_data

def get_phone (request):
	form = User_data(request.POST)
	if form.is_valid():
		# validation depends on the member variable being querried...
		# (figure that out and put some stuff here)
	return HttpResponseRedirect('/complete/')
