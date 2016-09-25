from django.contrib.sessions import middleware
from django.contrib.sessions.models import Session
from django.conf import settings
from django.core.urlresolvers import reverse
from .models import User
import plivo

# need to discuss
def _load_and_keep_session_key(orig):
	def wrapper(self):
		session_key = self.session_key
		result = orig(self)
		self._session_key = session_key

		return result

	return wrapper

def session_status_tracker(request):
	if hasattr(request, 'session'):
		if 'phone_num' in request.session:
			print "request.session['phone_num'] = %s" % request.session['phone_num']
			print "request.path_info = %s" % request.path_info
			print "request.session['active_urls'] = "
			for keys, values in request.session['active_urls'].items():
				print "%s:%s" % (keys, values)
			if 'default_data' in request.session.keys():
				print "request.session['default_data'] = %s" % request.session['default_data']
			else:
				print "request.session['default_data'] = (empty)"
		else:
			print "request.session['phone_num'] = (empty)"
	else:
		print "New session."

class SmsSessionMiddleware(middleware.SessionMiddleware):
	def __init__(self):
		super(SmsSessionMiddleware, self).__init__() # discuss purpose of super on __init__()
		self.SessionStore.load = _load_and_keep_session_key(self.SessionStore.load)

	def process_request(self, request):
		print 'beginning of process_request()'

		session_key = request.POST.get('From', request.COOKIES.get(settings.SESSION_COOKIE_NAME))

		request.session = self.SessionStore(session_key=session_key) # does SessionStore erase existing session w/ same session key?
		request.session["phone_num"] = session_key

		request.session.set_expiry(300)

		message_content = request.POST.get('Body')
		messageuuid = request.POST.get('MessageUUID')

		print 'message_content = %s' % message_content

		if 'active_urls' in request.session:
			if message_content in request.session['active_urls']:
				request.path_info = request.session['active_urls'][message_content]
				request.session['active_urls'] = {}

				print "first option."
				session_status_tracker(request)

			else:

				if 'default_url' in request.session['active_urls']:
					request.session['default_data'] = message_content
					request.path_info = request.session['active_urls']['default_url']
					print 'Default_url in request.session. End of process_request().'
					session_status_tracker(request)

				else:
					if len(request.session['active_urls']) == 0:
						request.path_info = '/topmenu/menu_2/'

						print "3rd option."
						session_status_tracker(request)

					else:
						request.path_info = '/topmenu/invalid_response/'
						print "Invalid response."
						session_status_tracker(request)

		else:
			request.path_info = '/topmenu/menu_2/'
			request.session['active_urls'] = {}

			session_status_tracker(request)

