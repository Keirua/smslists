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
from django.db.models import Q



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

def send_message(request, source, destination, menu_text):
	p = plivo.RestAPI(auth_id, auth_token)
	params = {
    'src': source,  # Sender's phone number with country code
    'dst': destination,  # Receiver's phone Number with country code
    'text' : menu_text, # Your SMS Text Message - English
    'url' : "", # The URL to which with the status of the message is sent
    'method' : 'POST' # The method used to call the url
	}
	response = p.send_message(params)
	request.session['last_message'] = menu_text
	return response

@csrf_exempt
def session_flush(request):
	#immediately clear session
	print "Clearing session data."
	
	request.session.flush()
	reverse('topmenu:menu_2')

	return HttpResponse(status=200)

@csrf_exempt
def menu_2(request): 

	phone_num = request.session['phone_num'] or '12345678901'

	TOP_MENU_URLS = {
		"1": reverse('topmenu:listings', kwargs={"category": "for_sale"}),
		"2": reverse('topmenu:listings', kwargs={"category": "jobs"}),
		"3": reverse('topmenu:listings', kwargs={"category": "rides"}),
		"4": reverse('topmenu:listings', kwargs={"category": "announcements"}),
		"5": reverse('topmenu:voted_listings', kwargs={'category': 'commentary'}),
		"6": reverse('topmenu:voted_listings', kwargs={'category': 'emergency'}),
		"0": reverse('topmenu:user_dashboard'),
		# special development session flush
		"000": reverse('topmenu:session_flush'),
	}

	if  User.objects.filter(phone_num=phone_num).count() == 0:
		print "menu_2/create_user"
		
		User.objects.create(phone_num=phone_num, user_loc='Los Angeles')

		current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language]
		
		request.session['active_urls'].clear()
		request.session['active_urls'] = TOP_MENU_URLS

		menu_text = "1. %s, 2. %s, 3. %s, 4. %s, 5. %s, 6. %s, 0. User dashboard" % (current_language.for_sale, 
			current_language.jobs, current_language.rides, 
			current_language.announcements, current_language.commentary, 
			current_language.emergency)
		
		send_message(request, source=PLIVO_NUMBER, destination=phone_num,
		menu_text=menu_text)
		return HttpResponse(status=200)

	else:
		print "menu_2()"
		current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language]

		request.session["active_urls"].clear()
		request.session["active_urls"] = TOP_MENU_URLS

		menu_text = "1. %s, 2. %s, 3. %s, 4. %s, 5. %s, 6. %s, 0. User dashboard" % (current_language.for_sale,
		current_language.jobs, current_language.rides,
		current_language.announcements, current_language.commentary, 
		current_language.emergency)

		send_message(request, source=PLIVO_NUMBER, destination=phone_num,
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
	print "category = %s" % category

	post_message = '5. Post'
	back_message = '6. Back'
	search_message = '7. Search'

	displayed_items=[]

	request.session["active_urls"].clear()

	for counter, listing in enumerate((Listing.objects.filter(category=category).order_by('-pub_date')[:4]), start=1):

		request.session["active_urls"][counter] = reverse('topmenu:listing_detail', kwargs={'category':category, 'listing_id':listing.pk})
		displayed_items.append("%s. %s" % (counter, listing.header))

	request.session['active_urls'][5] = reverse('topmenu:post_subject_request', kwargs={'category':category})
	request.session['active_urls'][6] = reverse('topmenu:menu_2')
	request.session['active_urls'][7] = reverse('topmenu:search_request', kwargs={'category':category})

	displayed_items.append('5. Post 6. Back')
	displayed_items = "\n".join(displayed_items)


	if len(displayed_items) == 0:
		displayed_items = 'No active listings in %s. 5. Post 6. Back' % category
	else:
		pass
	# debug code/
	print "displayed_items = "+displayed_items
	print 'ACTIVE URLS = '+str(request.session['active_urls'])
	# /debug code

	send_message(request, PLIVO_NUMBER, request.session["phone_num"], displayed_items)
	return HttpResponse(status=200)


@csrf_exempt
def listing_detail(request, category, listing_id, from_dashboard=False):
	print "listing_detail"
	"""
	2. Using pk in link, call db and pull full
	entry. Send SMS and map possible corresponding possible link responses.
	Update session.
	"""
	displayed_items = []
	delete_message = '7. Delete listing.'

	request.session['active_urls'].clear()
	request.session['active_urls'][6] = reverse('topmenu:listings', kwargs={'category':category})

	listing = Listing.objects.get(pk=listing_id)

	if from_dashboard = True:
		request.session['active_urls'][7] = Listing.is_active(False)



	send_message(request, PLIVO_NUMBER, request.session['phone_num'], listing.detail+' 6. Back')
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
	send_message(request, PLIVO_NUMBER, request.session['phone_num'], post_message_1)
	return HttpResponse(status=200)
	
@csrf_exempt
def post_description_request(request, category):
	"""
	Collect user subject and map to session. Send user SMS requesting listing
	description. Set "active_urls "default_url" key to value 
	("topmenu:post_review").
	"""

	post_message_2 = "Listing description? (max 140 characters) Reply '9' to return to main menu."
	cancellation_message = "Listing cancelled. Returning to main menu."


	if request.session['default_data'] == '9':

		del request.session['active_urls']['default_url']
		del request.session['default_data']

		send_message(request, PLIVO_NUMBER, request.session["phone_num"], cancellation_message)
		reverse('topmenu:menu_2')
		return HttpResponse(status=200)

	else:

		request.session["new_post_subject"] = request.session["default_data"]
		request.session["active_urls"]["default_url"] = reverse("topmenu:post_review", 
			kwargs={'category':category})

		send_message(request, PLIVO_NUMBER, request.session["phone_num"], post_message_2)
		return HttpResponse(status=200)

@csrf_exempt
def post_review(request, category):
	"""
	Collect user description and map to session. Send user post subject and
	description for review. Set "active_urls "default_url" key to value 
	("topmenu:post_commit").
	"""
	cancellation_message = "Listing cancelled. Returning to main menu."

	if request.session['default_data'] == '9':
		del request.session['active_urls']['default_url']
		del request.session['default_data']
		del request.session['new_post_subject']

		send_message(request, PLIVO_NUMBER, request.session["phone_num"], cancellation_message)
		reverse('topmenu:menu_2')
		return HttpResponse(status=200)

	else:
		request.session['new_post_description'] = request.session['default_data']
		request.session["active_urls"]["default_url"] = reverse("topmenu:post_commit", kwargs={'category':category})
		
		post_message_3 = "Please review your listing."
		post_message_4 = "Subject: %s" % request.session["new_post_subject"]
		post_message_5 = "Description: %s" % request.session["new_post_description"]
		post_message_6 = "'1' to confirm listing or '9' to delete listing and return to main menu."

		send_message(request, PLIVO_NUMBER, request.session["phone_num"], post_message_3)
		time.sleep(0.5)
		send_message(request, PLIVO_NUMBER, request.session["phone_num"], post_message_4)
		time.sleep(0.5)
		send_message(request, PLIVO_NUMBER, request.session["phone_num"], post_message_5)
		time.sleep(0.5)
		send_message(request, PLIVO_NUMBER, request.session["phone_num"], post_message_6)
		return HttpResponse(status=200)

@csrf_exempt
def post_commit(request, category):
	"""
	"""
	confirmation_message = "Listing successfully posted in %s." % category
	cancellation_message = "Listing cancelled. Returning to main menu."
	invalid_input = "Input not recognized. Reply '1' to confirm posting or '9' to cancel."

	print "request.session['default_data'] ="+request.session['default_data']
	if request.session['default_data'] == '1': 
		Listing.objects.create(header=request.session['new_post_subject'], 
			detail=request.session['new_post_description'], category=category,
			owner=User.objects.get(phone_num=request.session['phone_num']))
		send_message(request, PLIVO_NUMBER, request.session['phone_num'], confirmation_message)
		menu_2(request)
		return HttpResponse(status=200)
	
	# can't parse message request in middleware, so menu_2 redirect here:
	elif request.session['default_data'] == '9': # changed from request.POST
		send_message(request, PLIVO_NUMBER, request.session['phone_num'], cancellation_message)
		
		del request.session['active_urls']['default_url']
		del request.session['default_data']
		del request.session['new_post_subject']
		del request.session['new_post_description']

		menu_2(request)
		return HttpResponse(status=200)
	
	else:
		send_message(request, PLIVO_NUMBER, request.session["phone_num"], invalid_input)
		request.session["active_urls"]["default_url"] = reverse("topmenu:post_commit", 
			kwargs={'category':category})
		return HttpResponse(status=200)

@csrf_exempt
def invalid_response(request):
	"""If user submits a response not in active_urls, system resends last
	message and a second message with active commands.
	"""
	print "/topmenu/invalid_response/"
	send_message(request, PLIVO_NUMBER, request.session['phone_num'], request.session['last_message'])
	return HttpResponse(status=200)

@csrf_exempt
def user_dashboard(request, default_lower_bound=None, default_upper_bound=4):
	"""Allows user to view and delete their active listings.
	"""

	request.session['active_urls'].clear()
	request.session['active_urls'][6] = reverse('topmenu:menu_2')

	user_listings_clean = []
	numbered_list = [1, 2, 3, 4]
	displayed_items = []
	next_message = "5. Next"
	back_message = "6. Back"

	user_listings_raw = Listing.objects.filter(owner_id=(User.objects.filter(
		request.session['phone_num'])).values_list('id'))[default_lower_bound:default_upper_bound]

	# set listings 'active_urls'
	for counter, listing in enumerate(user_listings_raw, start=1):
		request.session['active_urls'][counter] = reverse('topmenu:listing_detail', kwargs={'listing_id':listing.pk, 'from_dashboard':True})

	# format sms
	for x, y in user_listings_raw.values_list('header', 'pub_date'):
		user_listings_clean.append(("%s, %s/%s/%s") % (x, y.month, y.day, y.year))

	final_list = zip(numbered_list, user_listings_clean)

	for x, y in final_list:
		displayed_items.append("%s. %s" % (x, y))


	if default_upper_bound < len(user_listings_raw):

		displayed_items.append(next_message)

		default_lower_bound = default_lower_bound + 4
		default_upper_bound = default_upper_bound + 4

		request.session['active_urls'][5] = reverse('topmenu:user_dashboard', 
			kwargs={'default_lower_bound':default_lower_bound, 'default_upper_bound':default_upper_bound})
	
	else:
		# do nothing because there are either no more pages of results to show
		# or only one page total of results
		pass

	displayed_items.append(back_message)
	displayed_items = "\n".join(displayed_items)

	send_message(request, PLIVO_NUMBER, request.session["phone_num"], displayed_items)
	return HttpResponse(status=200)

@csrf_exempt
def search_request(request, category):
	
	search_request_message = '%s search term? 6. Back' % category

	request.session['active_urls'].clear()
	request.session['active_urls'][6] = reverse('topmenu:listings', kwargs={'category':category})


	send_message(request, PLIVO_NUMBER, request.session['phone_num'], search_request_message)
	request.session['active_urls']['default_url'] = reverse('topmenu:search_results', kwargs={'category':category})
	return HttpResponse(status=200)
	
@csrf_exempt
def search_results(request, category, default_lower_bound=None, default_upper_bound=4):

	displayed_items = []
	results_raw = []
	next_message = "5. Next"
	back_message = "6. Back"

	for counter, listing in enumerate((Listing.objects.filter(Q(category__exact=category), Q(header__icontains=request.session['default_data'])
		| Q(detail__icontains=request.session['default_data'])).order_by('-pub_date')[default_lower_bound:default_upper_bound]), start=1):
		
		request.session['active_urls'][counter] = reverse('topmenu:listing_detail', kwargs={'category':category, 'listing_id':listing.pk})
		displayed_items.append('%s. %s' % (counter, listing.header))

	if default_upper_bound < len(displayed_items):

		displayed_items.append(next_message)

		default_lower_bound = default_lower_bound + 4
		default_upper_bound = default_upper_bound + 4

		request.session['active_urls'][5] = reverse('topmenu:user_dashboard', 
			kwargs={'default_lower_bound':default_lower_bound, 'default_upper_bound':default_upper_bound})

	else:
	# do nothing because there are either no more pages of results to show
	# or only one page total of results
		pass

	displayed_items.append(back_message)
	displayed_items = "\n".join(displayed_items)

	send_message(request, PLIVO_NUMBER, request.session['phone_num'], displayed_items)
	return HttpResponse(status=200)
