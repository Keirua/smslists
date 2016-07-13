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

@csrf_exempt
def menu_2(request): # 7/9 changed phone_num to session_key.
	phone_num = request.session["phone_num"]
	# get user language
	current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language] #ADD THIS TO SESSION
	print "def menu_2()"

	request.session["active_urls"][1]="/listings/for_sale/"
	request.session["active_urls"][2]="/listings/wanted/"
	request.session["active_urls"][3]="/listings/jobs/"
	request.session["active_urls"][4]="/listings/announcements/"
	# request.session["5."]="/post/"

	for link_value, url in request.session["active_urls"].items():
		if link_value < 5:
			print "link_value "+str(link_value)+" is "+str(url)

	if "active_urls" in request.session:
		print True
	else:
		print False

	menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale, 
		current_language.wanted, current_language.jobs,
		current_language.announcements)

	send_message(source = PLIVO_NUMBER, destination=phone_num,
		menu_text=menu_text)
	return HttpResponse(status=200)

	# RECEIVE (need to build)


@csrf_exempt
def listings(request, category):
	"""
	2 possible paths:
	
	1. No listings stored in session (message_content=None); Pull location and
	category from session; call db and pull 4 entries and generate link from
	pk; map links to user-viewable commands and send; update session.
	"""

	print "def listings()"

	# location = User.user_loc.get(phone_num)
	
	displayed_items=[]
	# Listings.objects.order_by('-pub_date')[:4]

	for counter, listing in enumerate(Listings.objects.order_by('-pub_date')[:4]):
		request.session["active_urls"][counter] = reverse(name="for_sale", kwargs={'id':listing.pk}) # <- correct method to pass kwargs to subdomaine?
		displayed_items.append("%s. %s" % (counter, listing.header))

	displayed_items = "\n".join(displayed_items)
# DEBUG PRINT
	print "displayed_items = "+displayed_items
# DEBUG PRINT
	send_message(PLIVO_NUMBER, request.session["phone_num"], displayed_items)
	return HttpResponse(status=200)



@csrf_exempt
def listing_detail(session_key, category, message_content):
	"""
	2. Listings already stored in session; Parse message context and map
	user to corresponding link. Using pk in link, call db and pull full
	entry. Send SMS and map possible corresponding possible link responses.
	Update session.
	"""


# def search(request):
#	Items.objects.filter(location=request.GET['location'], id_get=int(request.GET['first_id']))[:4] 




