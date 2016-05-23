from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing, Listing_detail
from django.http import Http404

def index(request):
	latest_listing_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_listing_list': latest_listing_list,}
	render(request, 'topmenu/index.html', context)