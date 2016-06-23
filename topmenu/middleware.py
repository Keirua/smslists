from django.contrib.sessions import middleware

class SmsLinkHandlerMiddleware(object): 
	def process_request(self, request):
		messageuuid = request.POST['MessageUUID']
		message_content = request.POST['Text']

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def process_request(self, request):
		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))
		request.session = self.SessionStore(session_key)

		"""
		ALT VERSION OF ^
		if 'From' in request.POST:
    		session_key = request.POST['From']
		else:
    		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    	"""

class 

request.Session["user_state"]="menu_2"
return HttpResponseRedirect("/topmenu/")