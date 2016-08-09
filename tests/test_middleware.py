import unittest
from topmenu import middleware 
from mock import Mock

class SmsSessionMiddlewareTest(unittest.TestCase):
	def setUp(self):
		self.ssm = middleware.SmsSessionMiddleware()
		self.request = Mock()
		self.request.session = {}

	def test___init__(self):
		pass

	def test_process_request_new_session(self):
		"""
		Process request with a new session should return None.
		Session is instantiated and exists as an attribute of request."""
		self.assertEqual(self.ssm.process_request(self.request), None)
		self.assertIsInstance(self.request.session, self.ssm.session) # correct way to access Session object?

	def test_process_request_existing_session(self):
		"""Process request with an existing session should return None.
		Session is intantiated and exists as an attribute of request. phone_num
		is accessible within session."""
		self.request.session['phone_num'] = 18182857345
		self.assertEqual(self.ssm.process_request(self.request), None)
		self.assertIsInstance(self.request.session, self.ssm.session)
		self.assertEqual(self.request.session[phone_num], self.request.session[phone_num])
		self.assertEqual(self.ssm.process_request(self.request).session_key, self.request.session['phone_num'])
		self.assertIn(self.ssm.process_request(self.request))

	def test_process_request_existing_session_and_active_urls_not_present(self):
		"""If 'active_urls' not in request.session, path_info should be to
		create_user. 'active_urls' should be added to request.session."""
		

		self.assertNotIn('active_urls', self.request.session)
		self.ssm
		self.assertEqual(self.ssm.process_request(self.request)


request.path_info = "/topmenu/menu_2/create_user/"
			request.session["active_urls"] = {}

# how to test further along a method

	def test_process_request_

if __name__ = '__main__':
	unittest.main()



