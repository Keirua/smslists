from django.contrib.sessions import middleware
from django.contrib.sessions.models import Session

class SmsLinkHandlerMiddleware(object): 
	def process_request(self, request):
		messageuuid = request.POST['MessageUUID']
		message_content = request.POST['Text']

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def process_request(self, request):
		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))
		request.session = self.SessionStore(session_key)
		message_content = request.POST['Text']
		request.path_info = '/topmenu/'
		
		"""
		ALT VERSION OF ^
		if 'From' in request.POST:
    		session_key = request.POST['From']
		else:
    		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    	"""
		
		if request.session['last_login'] == None:



		

    	reverse(views.listings, kwargs=)
    	RL)

"""
class AdminRequest(middleware.SessionMiddleware):
	def filter_admin(self, session_key):
		if len(session_key) != 10:
		return HttpResponseRedirect("/admin", status=200)
"""

# SmsSessionMiddleware will handle redirect to menus, but need to build out smscontextfinder to handle commands
class SmsContextFinder(middleware.SessionMiddleware):
	def get_user_state(self, session_key):
		user_state = request.session["user_state"] 
		fav_color = request.session["fav_color"]

### example code:
request.Session["user_state"]="menu_2"
return HttpResponseRedirect("/topmenu/menu_2", status=200) # need to change topmenu/urls.py (currently everything points to plivo endpoint)


session = Session.objects.get(pk=request.session._session_key)
