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
from middleware import PlivoHandler


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

def menu_2(session_key): # 7/9 changed phone_num to session_key.
	# get user language
	current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language] #ADD THIS TO SESSION
	
	# SEND
	request.session["1."]="/listings/for_sale/"
	request.session["2."]="/listings/wanted/"
	request.session["3."]="/listings/jobs/"
	request.session["4."]="/listings/announcements/"
	# request.session["5."]="/post/"

	menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale, 
		current_language.wanted, current_language.jobs,
		current_language.announcements)

	send_message(source = PLIVO_NUMBER, destination=phone_num,
		menu_text=menu_text)
	return HttpResponse(status=200)

	# RECEIVE (need to build)



def listings(session_key, category, message_content=None):
	"""
	2 possible paths:
	
	1. No listings stored in session (message_content=None); Pull location and
	category from session; call db and pull 4 entries and generate link from
	pk; map links to user-viewable commands and send; update session.
	
	2. Listings already stored in session; Parse message context and map
	user to corresponding link. Using pk in link, call db and pull full
	entry. Send SMS and map possible corresponding possible link responses.
	Update session.
	"""

	# get user location

	phone_num = session_key
	location = User.user_loc.get(phone_num)

	if message_content == None:
		# linkxyz = reverse(location, category, pk) <- goal
		link1 = reverse("%s", Listings.header.filter(location, category, [-1:]) % category # need to return the last db item's pk where location and category match
		link2 = Listings.header.filter(location, category, [-2:-1])
		link3 = Listings.header.filter(location, category, [-3:-2])
		Link4 = Listings.header.filter(location, category, [-4:-3])




def search(request):
	Items.objects.filter(location=request.GET['location'], id_get=int(request.GET['first_id']))[:4] #where are location and first_id defined?





