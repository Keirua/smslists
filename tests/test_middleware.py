import unittest
from topmenu import middleware
from mock import Mock

class SmsSessionMiddlewareTest(unittest.TestCase):
	def setUp(self):
		self.ssm = middleware.SmsSessionMiddleware()
		self.request = unittest.mock
		self.request.session = {}

	def test___init__(self):
		pass

	def test_process_request_new_session(self):
		"""Process request with a new session should return None.
		Session is instantiated and added as an attribute of request."""
		self.assertEqual(self.ssm.process_request(self.request), None)
		self.assertIsInstance(self.request.session, SmsSessionMiddleware)

	def test_process_request_existing_session(self):
		"""Process request with an existing session should return None."""
		self.assertEqual(self.ssm.process_request(self.request), None)
		self.assertIsInstance(self.request.session, Session)
		self.assertEqual(self.request.session[phone_num], request.session[phone_num])

		



