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

		"""
		ALT VERSION OF ^
		if 'From' in request.POST:
    		session_key = request.POST['From']
		else:
    		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    	"""
    	# if session is empty, send to menu_2. NOTE: will need to pass in source for views arguments. NOTE2: don't think redirects to submenus (i.e.
    		# browsing listings) will be necessary, but will think about it.
    	if session_key == None:
    		return HttpResponseRedirect("topmenu/menu_2", status=200) # 'else' criteria needed?
    	else:
    		user_state = request.Session.get['user_state']
    		if user_state == "menu_2":
				return HttpResponseRedirect("/topmenu/menu_2", status=200)
			elif user_state == "listings":
				return HttpResponseRedirect("/topmenu/listings", status=200)
			elif user_state == "wanted":
				return HttpResponseRedirect("/topmenu/wanted", status=200)
			elif user_state == "jobs":
				return HttpResponseRedirect("/topmenu/jobs", status=200)
			elif user_state == "announcements":
				return HttpResponseRedirect("/topmenu/announcements", status=200)

class AdminRequest(middleware.SessionMiddleware)
	def filter_admin(self,session_key):
		if len(session_key) != 10:
		return HttpResponseRedirect("/admin", status=200)

# SmsSessionMiddleware will handle redirect to menus, but need to build out smscontextfinder to handle commands
class SmsContextFinder(middleware.SessionMiddleware)
	def get_user_state(self, session_key):
		user_state = request.session["user_state"] 
		fav_color = request.session["fav_color"]

### example code:
request.Session["user_state"]="menu_2"
return HttpResponseRedirect("/topmenu/menu_2", status=200) # need to change topmenu/urls.py (currently everything points to plivo endpoint)


session = Session.objects.get(pk=request.session._session_key)
