from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .models import Listing, User
from django.http import Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .languages import *
import plivo, time



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
def session_flush(request):
	#immediately clear session
	print "Clearing session data."
	
	request.session.flush()
	reverse('topmenu:menu_2')

	return HttpResponse(status=200)

@csrf_exempt
def menu_2(request, create_user=False): 

	# This could be a constant at the top of the file, but then it will cause a circular import problem
	TOP_MENU_URLS = {
		"1": reverse('topmenu:listings', kwargs={"category": "for_sale"}),
		"2": reverse('topmenu:listings', kwargs={"category": "wanted"}),
		"3": reverse('topmenu:listings', kwargs={"category": "jobs"}),
		"4": reverse('topmenu:listings', kwargs={"category": "announcements"}),
		# special development session flush
		"00": reverse('topmenu:session_flush'),
	}

	
	if create_user is not False:
		print "menu_2/create_user"
		if request.session['phone_num'] == None:
			request.session['phone_num'] = '12345678901'
			User.objects.get_or_create(phone_num='12345678901', user_loc='Los Angeles')
		else:
			User.objects.get_or_create(phone_num=phone_num, user_loc='Los Angeles')
		
		phone_num = request.session['phone_num']

		current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language]
		
		request.session['active_urls'].clear()
		request.session['active_urls'] = TOP_MENU_URLS

		menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale,
		current_language.wanted, current_language.jobs, 
		current_language.announcements)
		
		send_message(source=PLIVO_NUMBER, destination=phone_num,
		menu_text=menu_text)
		return HttpResponse(status=200)

	else:
		print "menu_2()"
		current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language]

		request.session["active_urls"].clear()
		request.session["active_urls"] = TOP_MENU_URLS

		menu_text = "1. %s, 2. %s, 3. %s, 4. %s" % (current_language.for_sale,
		current_language.wanted, current_language.jobs,
		current_language.announcements)

		send_message(source=PLIVO_NUMBER, destination=phone_num,
		menu_text=menu_text)
		return HttpResponse(status=200)

@csrf_exempt
def listings(request, category):
	"""
	2 possible paths:

	1. No listings stored in session (message_content=None); Pull location and
	category from session; call db and pull 4 entries and generate link from
	pk; map links to user-viewable commands and send; update session.
	"""
	print "listings()"

	displayed_items=[]

	# must go before listings text and links are generated
	request.session["active_urls"].clear()

	for counter, listing in enumerate(Listing.objects.order_by('-pub_date')[:4]):
		request.session["active_urls"][str(counter)] = reverse(
			'topmenu:listing_detail', kwargs={'id':listing.pk, 'category':category}
		)
		displayed_items.append("%s. %s" % (counter, listing.header))

	# TODO: handle the case when there are no items in the listing categor

	request.session["active_urls"][5] = reverse('topmenu:post_subject_request', kwargs={'category':category})
	request.session["active_urls"][6] = reverse('topmenu:menu_2')

	displayed_items = "\n".join(displayed_items)

	# debug code/
	print "displayed_items = "+displayed_items
	# /debug code

	send_message(PLIVO_NUMBER, request.session["phone_num"], displayed_items)
	return HttpResponse(status=200)


@csrf_exempt
def listing_detail(request, category, listing_id):
	"""
	2. Using pk in link, call db and pull full
	entry. Send SMS and map possible corresponding possible link responses.
	Update session.
	"""
	request.session['active_urls'].clear()
	request.session['active_urls'][6] = reverse('topmenu:listings')

	send_message(PLIVO_NUMBER, request.session['phone_num'], Listing.objects.detail(listing_id))
	return HttpResponse(status=200)

@csrf_exempt
def post_subject_request(request, category):
	"""
	Send user SMS requesting listing subject. Set 'active_urls' 'default_url'
	key to value reverse('topmenu:post_description_request'). 
	Return HttpResponse 200.
	"""
	# all user text will be migrated to locale directory
	post_message_1 = "Listing subject? (max 40 characters) Reply '9' to return to main menu."

	request.session['active_urls'].clear()
	request.session['active_urls']['default_url'] = reverse('topmenu:post_description_request', kwargs={'category':category})
	send_message(PLIVO_NUMBER, request.session['phone_num'], post_message_1)
	return HttpResponse(status=200)
	
@csrf_exempt
def post_description_request(request, category):
	"""
	Collect user subject and map to session. Send user SMS requesting listing
	description. Set "active_urls "default_url" key to value 
	("topmenu:post_review").
	"""

	post_message_2 = "Listing description? (max 140 characters) Reply '9' to return to main menu."

	if request.session['default_data'] == '9':
		del request.session['active_urls']['default_url']
		del request.session['default_data']
		del request.session['new_post_subject']
		del request.session['new_post_description']

		reverse('topmenu:menu_2')
		return HttpResponse(status=200)
	else:
		request.session["new_post_subject"] = request.session["default_data"]
		request.session["active_urls"]["default_url"] = reverse("topmenu:post_review", 
			kwargs={'category':category})
		send_message(PLIVO_NUMBER, request.session["phone_num"], post_message_2)
		return HttpResponse(status=200)

@csrf_exempt
def post_review(request, category):
	"""
	Collect user description and map to session. Send user post subject and
	description for review. Set "active_urls "default_url" key to value 
	("topmenu:post_commit").
	"""

	post_message_3 = "Please review your listing."
	post_message_4 = "Subject: %s" % request.session["new_post_subject"]
	post_message_5 = "Description: %s" % request.session["new_post_description"]
	post_message_6 = "'1' to confirm listing or '9' to delete listing and return to main menu."

	if request.session['default_data'] == '9':
		del request.session['active_urls']['default_url']
		del request.session['default_data']
		del request.session['new_post_subject']
		del request.session['new_post_description']

	else:
		request.session['new_post_description'] = request.session['default_data']
		request.session["active_urls"]["default_url"] = reverse("topmenu:post_commit", kwargs={'category':category})
		
		send_message(PLIVO_NUMBER, request.session["phone_num"], post_message_3)
		time.sleep(0.5)
		send_message(PLIVO_NUMBER, request.session["phone_num"], post_message_4)
		time.sleep(0.5)
		send_message(PLIVO_NUMBER, request.session["phone_num"], post_message_5)
		time.sleep(0.5)
		send_message(PLIVO_NUMBER, request.session["phone_num"], post_message_6)
		return HttpResponse(status=200)

@csrf_exempt
def post_commit(request, category):
	"""
	"""
	confirmation_message = "Listing successfully posted in %s." % category
	cancellation_message = "Listing cancelled. Returning to main menu."
	invalid_input = "Input not recognized. Reply '1' to confirm posting or '9' to cancel."

	print "request.session['default_data'] ="+str(request.session['default_data'])
	if request.session['default_data'] == '1': # changed from request.POST
		Listing.objects.create(header=request.session['new_post_subject'], 
			detail=request.session['new_post_description'], category=category)
		send_message(PLIVO_NUMBER, request.session['phone_num'], confirmation_message)
		request.session['active_urls']['default_url'] = reverse('topmenu:menu_2')
		return HttpResponse(status=200)
	
	# can't parse message request in middleware, so menu_2 redirect here:
	elif request.session['default_data'] == '9': # changed from request.POST
		send_message(PLIVO_NUMBER, request.session['phone_num'], cancellation_message)
		
		del request.session['active_urls']['default_url']
		del request.session['default_data']
		del request.session['new_post_subject']
		del request.session['new_post_description']

		reverse('topmenu:menu_2')
		return HttpResponse(status=200)
	
	else:
		send_message(PLIVO_NUMBER, request.session["phone_num"], invalid_input)
		request.session["active_urls"]["default_url"] = reverse("topmenu:post_commit", 
			kwargs={'category':category})
		return HttpResponse(status=200)






