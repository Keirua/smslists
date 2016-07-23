from django.contrib.sessions import middleware
from django.contrib.sessions.models import Session
from django.conf import settings
from django.core.urlresolvers import reverse
import plivo

# need to discuss
def _load_and_keep_session_key(orig):
	def wrapper(self):
		session_key = self.session_key
		result = orig(self)
		self._session_key = session_key

		return result

	return wrapper

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def __init__(self):
		super(SmsSessionMiddleware, self).__init__() # discuss purpose of super on __init__()
		self.SessionStore.load = _load_and_keep_session_key(self.SessionStore.load)

	def process_request(self, request):

		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))

		request.session = self.SessionStore(session_key=session_key)
		request.session["phone_num"] = session_key

		# 5 min session expiration time
		request.session.set_expiry(300)

		message_content = request.POST['Text']
		messageuuid = request.POST['MessageUUID']

		if "active_urls" not in request.session:
			request.path_info = "/topmenu/menu_2/"
			request.session["active_urls"] = {}
			
		else:
			if "default_url" in request.session:
				request.POST["default_data"] = message_content
				request.path_info = active_urls["default_url"]
			else:
				request.path_info = request.session["active_urls"]
