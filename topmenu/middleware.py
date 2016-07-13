from django.contrib.sessions import middleware
from django.contrib.sessions.models import Session
from django.conf import settings
from django.core.urlresolvers import reverse

class SmsLinkHandlerMiddleware(object): 
	def process_request(self, request):
		messageuuid = request.POST['MessageUUID']
		message_content = request.POST['Text']

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def process_request(self, request):
		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))
		request.session = self.SessionStore(session_key)
		# session is created ^, now can store phone_num in session

		request.session["phone_num"] = session_key
		if 'active_urls' not in request.session:
			# request.path_info = reverse('menu_2')
			request.path_info = '/topmenu/menu_2/'
			request.session["active_urls"] = {}
		else:
			request.path_info = request.session["active_urls"][int(message_content)] # rather than int, change to str in dictionary
			# insert catch if user puts in value other than dictionary
			# remove extra spaces from user's input

		
"""
class PlivoHandler(object):
	def process_request(self, request): 
	@csrf_exempt
	@require_POST
	source = request.POST['From']
	destination = request.POST['To']
	messageuuid = request.POST['MessageUUID']
	message_content = request.POST['Text']
"""



