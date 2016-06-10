from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing, User # will this subclass include all attributes and imports for the parent class?
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .languages import *
import plivo
from django.db import models # attempt 1 to solve object attribute errors
import django.contrib.auth.models # attempt 2 to solve object attribute errors


PLIVO_NUMBER = "18058643381" # in the future will call deployment.txts
auth_id = "MANGVIYZY0ZMFIMTIWOG"
auth_token = "Yzc3OTgzZmU4MGIyNDI4ODgzMWE1MWExOWYxZTcx"



def index(request):
	print "index"
	latest_listing_list = Listing.objects.order_by('-pub_date')[:6]
	context = {'latest_listing_list': latest_listing_list,}
	return render(request, 'topmenu/index.html', context)

def detail(request, detail_id):
	print "detail"
	detail_display = get_object_or_404(Listing, pk = detail_id)
	return render(request, 'topmenu/detail.html', {'apples': detail_display})

# receieve sms method
@csrf_exempt
@require_POST
def plivo_endpoint(request):
	source = request.POST['From']
	destination = request.POST['To']
	messageuuid = request.POST['MessageUUID']
	message_content = request.POST['Text']

	try:
		User.objects.get(phone_num=source)
	except User.DoesNotExist:
		# create new User_data entry
		User.objects.create(phone_num=source, user_state=1)
		menu_text = ""
		send_message(source=destination, destination=source, menu_text="""
			Welcome! Your phone number has been recorded as %s""" % source)
		menu_2(source)
		return HttpResponse()
	else:
		menu_2(source)
		return HttpResponse()

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
	# update user state to reflect current menu 
	current_state = User.objects.filter(phone_num=phone_num).update(user_state=2)
	# current_state.save()
	current_language = User.objects.filter(phone_num=phone_num).get(User.user_language)
	menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale, 
		current_language.wanted, current_language.jobs, current_language.announcements)
	phone_num = reply_destination
	reply_source = Plivo_number
	send_message(reply_source, reply_destination, menu_text)
	return HttpResponse()






