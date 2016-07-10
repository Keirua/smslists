from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing, User 
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .languages import *
import plivo



PLIVO_NUMBER = "18058643381" # in the future will call deployment.txts
auth_id = "MANGVIYZY0ZMFIMTIWOG"
auth_token = "Yzc3OTgzZmU4MGIyNDI4ODgzMWE1MWExOWYxZTcx"


###############
def index(request):
	print "index"
	latest_listing_list = Listing.objects.order_by('-pub_date')[:6]
	context = {'latest_listing_list': latest_listing_list,}
	return render(request, 'topmenu/index.html', context)

def detail(request, detail_id):
	print "detail"
	detail_display = get_object_or_404(Listing, pk = detail_id)
	return render(request, 'topmenu/detail.html', {'apples': detail_display})
###############

def send_message(source, destination, menu_text):
	p = plivo.RestAPI(auth_id, auth_token)
	params = {
    'src': source,  # Sender's phone number with country code
    'dst': destination,  # Receiver's phone Number with country code
    'text' : menu_text, # Your SMS Text Message - English
    'url' : "", # The URL to which with the status of the message is sent
    'method' : 'POST' # The method used to call the url
	}
	response = p.send_message(params)	
	return response

def menu_2(phone_num):
	request.session["/topmenu/menu_2"]="/topmenu/menu_2" # don't need to store this. instead just store the 
	# get user language
	current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language] #ADD THIS TO SESSION

	request.session["1."]="/for_sale/"
	request.session["2."]="/wanted/"
	request.session["3."]="/jobs/"
	request.session["4."]="/announcements/"
	# request.session["5."]="/post/"

	menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale, 
		current_language.wanted, current_language.jobs,
		current_language.announcements)

	send_message(source = PLIVO_NUMBER, destination=phone_num,
		menu_text=menu_text)
	return HttpResponse(status=200)

def listings(request, id, category_name ):
	message_content == 


	if user_state==2:

def search(request):
	Items.objects.filter(location=request.GET['location'], id_get=int(request.GET['first_id']))[:4] #where are location and first_id defined?





