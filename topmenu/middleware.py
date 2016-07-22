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

		# 30 min session expiration time
		request.session.set_expiry(300)

		message_content = request.POST['Text']
		messageuuid = request.POST['MessageUUID']

		##############
		if "active_urls" not in request.session:
			request.path_info = '/topmenu/menu_2/'
			request.session["active_urls"] = {}
			
			# rewrite:
		else:
			if request.session["post_sequence"]["stage_1"] == True:
				if int(message_content) == 9:
					request.session["post_sequence"].clear()
					request.path_info = "/topmenu/menu_2"
				else:
					request.session["post_sequence"]["post_header"] = message_content
					request.path_info = "/topmenu/post_listing/"

			elif request.session["post_sequence"]["stage_2"] == True:
				if int(message_content) == 9:
					request.session["post_sequence"].clear()
					request.path_info = "/topmenu/menu_2"
				else:
					request.session["post_sequence"]["post_detail"] = message_content
					request.path_info = "/topmenu/post_listing/"

			elif request.session["post_sequence"]["stage_3"] == True:
				if int(message_content) == 9:
					request.session["post_sequence"].clear()
					request.path_info = "/topmenu/menu_2"
				else:
					request.session["post_sequence"]["post_conf"] = message_content
					request.path_info = "/topmenu/post_listing_commit/"
			else:
				request.path_info = request.session["active_urls"][message_content]

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



