from django.contrib.sessions import middleware
from django.contrib.sessions.models import Session

class SmsLinkHandlerMiddleware(object): 
	def process_request(self, request):
		messageuuid = request.POST['MessageUUID']
		message_content = request.POST['Text']

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def process_request(self, request):
		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))
		try request.session['session_key']: 
			except KeyError
			reverse('topmenu/menu_2/')
		else:
			request.session = self.SessionStore(session_key)
			message_content = request.POST['Text'] # does this need to go in plivo handler?
			request.path_info = '/topmenu/' # is this the right place for this?

			last_link1 = request.session.get["1."]
			last_link2 = request.session.get["2."]
			last_link3 = request.session.get["3."]
			last_link4 = request.session.get["4."]



		"""
		ALT VERSION OF ^
		if 'From' in request.POST:
    		session_key = request.POST['From']
		else:
    		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    	"""

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
