from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from .models import Listing, User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .languages import *
import plivo, time, twilio
from django.db.models import Q
from django.views.generic import View, ListView, TemplateView
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from twilio.rest import TwilioRestClient
from braces.views import CsrfExemptMixin
import twilio.twiml
from django.template.response import SimpleTemplateResponse
from django.db.models.query import QuerySet
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage, Paginator
from django.utils import six
from django.utils.translation import ugettext as _

 
# TWILIOAPI
ACCOUNT_SID = "AC0b5cdee16cd76023dd0784ca80fdbaa8" 
AUTH_TOKEN = "336894260c0040444134344d86886a3e"
PLIVO_NUMBER = "17472221816"
 



def send_message(request, source, destination, menu_text):
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
	client.messages.create(
	    to=destination, 
	    from_=source, 
	    body=menu_text,  
	)

	request.session['last_message'] = menu_text



class TwilioResponseMixin(object):
	def dispatch(self, request, *args, **kwargs):
      
		response = super(TwilioResponseMixin, self).dispatch(request, *args, **kwargs)
  		
  		# handle view returning httpresponse instead of string.
  		# this will allow more customizability if some functions return
  		# and others return httpresponse objects.

		if isinstance(response, HttpResponse):
			if isinstance(response, SimpleTemplateResponse):
				response.render()
			content = response.content
		
		elif isinstance(response, str):
			content = response

		twilio_response = twilio.twiml.Response()
		twilio_response.message(msg=content, to=request.session['phone_num'], 
			sender=PLIVO_NUMBER)
		response = HttpResponse(content=str(twilio_response))

		return response

#PLIVOAPI:
"""
PLIVO_NUMBER = "18058643381" # in the future will call deployment.txts
auth_id = "MANGVIYZY0ZMFIMTIWOG"
auth_token = "Yzc3OTgzZmU4MGIyNDI4ODgzMWE1MWExOWYxZTcx"
"""

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
#PLIVOAPI
""" 
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
"""

@csrf_exempt
def session_flush(request):
	#immediately clear session
	print "Clearing session data."
	
	request.session.flush()
	reverse('topmenu:menu_2')

	return HttpResponse(status=200)

class MainMenu(CsrfExemptMixin, TwilioResponseMixin, TemplateView):
	
	template_name = 'mainmenu.txt'

	def __init__(self, *args, **kwargs):

		super(MainMenu, self).__init__(*args, **kwargs)

		self.TOP_MENU_URLS = {
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

	# after being passed from below-written post method to generic view get(),
	# request and *args, **kwargs are passed are passed get_context_data(). 
	# After context dict is generated, render_to_response in TemplateResponseMixin
	# (method of TemplateView) applies context and returns back to TwilioResponseMixin.dispatch()
	def get_context_data(self, *args, **kwargs):
		
		phone_num = self.request.session['phone_num'] or '12345678901'

		if  User.objects.filter(phone_num=phone_num).count() == 0:
			print "menu_2/create_user"
			
			User.objects.create(phone_num=phone_num, user_loc='Los Angeles')

			current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language]
			
			self.request.session['active_urls'].clear()
			self.request.session['active_urls'] = self.TOP_MENU_URLS
			
			return {'current_language':current_language}

		else:
			print "menu_2()"
			current_language = LANGUAGES[User.objects.get(phone_num=phone_num).user_language]

			self.request.session["active_urls"].clear()
			self.request.session["active_urls"] = self.TOP_MENU_URLS
			print {'current_language':current_language}
			return {'current_language':current_language}

	# after dispatch, this is the first method to be called.
	def post(self, request, *args, **kwargs): 
			# return get method instead of post because 1 - at this point none
			# of the functional http request attributes matter (this is all
			# internal), 2 - this allows for the use of other generic views.
			# *args and **kwargs are whatever is appended in url config.
			return self.get(request, *args, **kwargs)


class Listings(CsrfExemptMixin, TwilioResponseMixin, ListView):

	template_name = 'listings.txt'

	paginate_by = 4

	ordering = '-pub_date'

	model = Listing

	def post(self, request, *args, **kwargs):
		self.request = request
		print 'def post KWARGS = %s' % kwargs
		return self.get(request, *args, **kwargs)

	def get_queryset(self):

		return super(Listings, self).get_queryset().filter(category=self.kwargs['category'], is_active=True)

	def get_context_data(self):

		print "listings()"
		print "category = %s" % self.kwargs['category']

		post_message = '5. Post'
		back_message = '6. Back'
		search_message = '7. Search'
		next_message = '8. Next'

		self.request.session["active_urls"].clear()
		print 'active_urls cleared!!!'

		#for counter, listing in enumerate((self.object_list), start=1):
		#	self.request.session['active_urls'][counter] = reverse('topmenu:listing_detail', kwargs={'category':self.kwargs['category'], 'listing_id':listing.pk})

		# self.request.session['active_urls'][5] = reverse('topmenu:post_subject_request', kwargs={'category':self.kwargs['category']})
		# self.request.session['active_urls'][6] = reverse('topmenu:menu_2')
		# self.request.session['active_urls'][7] = reverse('topmenu:search_request', kwargs={'category':self.kwargs['category']})

		listings = {}
		for listing in self.object_list:
			{'listing_id':listing.pk}

		context = super(Listings, self).get_context_data()
		print context
		context['category'] = self.kwargs['category']
		context['listing'] = {'listing_id':listing.pk}
		return context


@csrf_exempt
def listing_detail(request, category, listing_id, default_lower_bound=None, default_upper_bound=None, from_dashboard=False):
	print "listing_detail"
	"""
	2. Using pk in link, call db and pull full
	entry. Send SMS and map possible corresponding possible link responses.
	Update session.
	"""
	displayed_items = []
	delete_message = '7. Delete listing.'
	back_message = '6. Back'

	request.session['active_urls'].clear()
	request.session['active_urls'][6] = reverse('topmenu:listings', kwargs={'category':category})

	listing = Listing.objects.get(pk=listing_id)

	displayed_items.append(listing.detail)
	displayed_items.append(back_message)

	if from_dashboard == True:
		request.session['active_urls'][7] = Listing.is_active(False)
		request.session['active_urls'][6] = reverse('topmenu:user_dashboard', 
			kwargs={'default_lower_bound':default_lower_bound, 
			'default_upper_bound':default_upper_bound})
		displayed_items.append(delete_message)
	else:
		# act normally because not from_dashboard=True
		pass

	displayed_items = '\n'.join(displayed_items)

	send_message(request, PLIVO_NUMBER, request.session['phone_num'], displayed_items)
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

		request.session["new_post_subject"] = request.session["default_data"].strip()
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
		request.session['new_post_description'] = request.session['default_data'].strip()
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

	error_message = 'Not a valid command. Returning to main menu.'

	if 'last_message' in request.session: 

		send_message(request, PLIVO_NUMBER, request.session['phone_num'], request.session['last_message'])
		return HttpResponse(status=200)

	else:
		send_message(request, PLIVO_NUMBER, request.session['phone_num'], error_message)
		return MainMenu.as_view()(request)
		

class UserDashboard(ListView):
	pass

@csrf_exempt
def user_dashboard(request, default_lower_bound=0, default_upper_bound=4):
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
		request.session['phone_num'])), is_active=True).values_list('id')[default_lower_bound:default_upper_bound]

	# set listings 'active_urls'
	for counter, listing in enumerate(user_listings_raw, start=1):
		request.session['active_urls'][counter] = reverse(
			'topmenu:listing_detail', kwargs={'listing_id':listing.pk, 
			'from_dashboard':True, 'default_lower_bound':default_lower_bound,
			'default_upper_bound':default_upper_bound})

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

class SearchRequest(TwilioResponseMixin, View):

	def post(self, request, category):
		search_request_message = '%s search term? 6. Back' % category

		request.session['active_urls'].clear()
		request.session['active_urls'][6] = reverse('topmenu:listings', kwargs={'category':category})		
		request.session['active_urls']['default_url'] = reverse('topmenu:search_results', kwargs={'category':category})
		
		return search_request_message
"""
@csrf_exempt
def search_request(request, category):
	
	search_request_message = '%s search term? 6. Back' % category

	request.session['active_urls'].clear()
	request.session['active_urls'][6] = reverse('topmenu:listings', kwargs={'category':category})


	send_message(request, PLIVO_NUMBER, request.session['phone_num'], search_request_message)
	request.session['active_urls']['default_url'] = reverse('topmenu:search_results', kwargs={'category':category})
	return HttpResponse(status=200)
"""
	
@csrf_exempt
def search_results(request, category, default_lower_bound=0, default_upper_bound=4):

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

@csrf_exempt
def voted_listings(request, category, default_lower_bound=None, default_upper_bound=4):
	displayed_items = []
	in_development_message = '%s listings is still in development. Check back soon.' % (category.title())
	back_message = 'Press'

	displayed_items.append(in_development_message)
	displayed_items.append(back_message)

	time.sleep(2)


	displayed_items = '\n'.join(displayed_items)

	send_message(request, PLIVO_NUMBER, request.session['phone_num'], displayed_items)
	return HttpResponse(status=200)
