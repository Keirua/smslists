from django.contrib.sessions import middleware
from django.contrib.sessions.models import Session

class SmsLinkHandlerMiddleware(object): 
	def process_request(self, request):
		messageuuid = request.POST['MessageUUID']
		message_content = request.POST['Text']

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def process_request(self, request):
		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))
		
		# check to see if active session exists
		try request.session['session_key']: 
			except KeyError
			reverse('topmenu/menu_2/')

		# if active session exists, parse message content and map to context
		else:
			request.session = self.SessionStore(session_key)
			message_content = request.POST['Text'] # does this need to go in plivo handler or the SmsLinkHandlerMiddleware?
			request.path_info = '/topmenu/' # is this the right place for this?


			# find context

			# possible types of incoming urls:

			/menu_2/for_sale/
			/menu_2/wanted/
			/menu_2/jobs/
			/menu_2/announcements/

			/listings/234/ # for_sale item pk 234
			/listings/235/ # for_sale item pk 235
			/listings/723/

			/listings/for_sale/234


			last_link1 = request.session.get["1.", None]

			
			# last_link2 = request.session.get["2.", None]
			# last_link3 = request.session.get["3.", None]
			# last_link4 = request.session.get["4.", None]

			if 

			# PULL MESSAGE CONTENT AND REDIRECT TO CORRECT URL (BASED OFF CONTEXT)


		"""
		ALT VERSION OF ^
		if 'From' in request.POST:
    		session_key = request.POST['From']
		else:
    		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    	"""

    				# parse message conent

			if int(message_content) = 


class PlivoHandler(object):
	def process_request(self, request): 
	@csrf_exempt
	@require_POST
	source = request.POST['From']
	destination = request.POST['To']
	messageuuid = request.POST['MessageUUID']
	message_content = request.POST['Text']


### example code:
request.Session["user_state"]="menu_2"
return HttpResponseRedirect("/topmenu/menu_2", status=200) # need to change topmenu/urls.py (currently everything points to plivo endpoint)


session = Session.objects.get(pk=request.session._session_key)
