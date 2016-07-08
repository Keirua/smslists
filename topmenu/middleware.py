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

		"""
		ALT VERSION OF ^
		if 'From' in request.POST:
    		session_key = request.POST['From']
		else:
    		session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    	"""

    	reverse(views.listings, kwargs=)
    	
    	if session_key == None:
    		return HttpResponseRedirect("topmenu/menu_2", status=200)
    		user_state = request.Session.get['user_state']
    		
    		if user_state == "menu_2":
    			if message_content == 1:
    				return HttpResponseRedirect("/topmenu/listings", status=200)
    			elif message_content == 2:
    				return HttpResponseRedirect("/topmenu/wanted", status=200)
    			elif message_content == 3:
    				return HttpResponseRedirect("/topmenu/jobs", status=200)
    			elif message_content == 4:
    				return HttpResponseRedirect("/topmenu/announcements", status=200)
			
			elif user_state == "listings":
				if int(message_content)==1:
					# get URL that "1" corresponds to for this specific user search. need to build display results view(s). NEED TO ADD RESULTS PAGE TO DICTIONARY.
					# return HttpResponseRedirect( ^ this URL)
					# return HttpResponseRedirect("/topmenu/listings", status=200)
				elif int(message_content)==2:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==3:
					pass # etc etc etc
					# return HttpResponseRedirect(URL)
				elif int(message_content)==4:
					pass
					# return HttpResponseRedirect(URL)
			
			elif user_state == "wanted":
				if int(message_content)==1:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==2:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==3:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==4:
					# return HttpResponseRedirect(URL)
			
			elif user_state == "jobs":
				if int(message_content)==1:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==2:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==3:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==4:
					# return HttpResponseRedirect(URL)
			
			elif user_state == "announcements":
				if int(message_content)==1:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==2:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==3:
					pass
					# return HttpResponseRedirect(URL)
				elif int(message_content)==4:
					# return HttpResponseRedirect(URL)

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
