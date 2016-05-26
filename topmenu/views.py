from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing
from django.http import Http404

def index(request):
	print "index"
	latest_listing_list = Listing.objects.order_by('-pub_date')[:6]
	context = {'latest_listing_list': latest_listing_list,}
	return render(request, 'topmenu/index.html', context)

def detail(request, detail_id):
	print "detail"
	detail_template_activate = True

	return render(request, 'topmenu/detail.html', )

#	detail = get_object_or_404(Listing_detail, pk=detail_id)
#	return render(request, 'topmenu/detail.html', {'listing': listing})
