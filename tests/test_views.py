"""
Unit test for views.py
"""

from topmenu import views
from django.test.client import ClientHandler
import unitttest

class SessionHandler(ClientHandler):
	def get_response(self, request):
		response = super(SessionHandler, self).get_response(request)
		respon

class test_menu_2(unitttest.TestCase):
	def setUp(self):
		


from django.test import TestCase
from django.test.client import ClientHandler

class SessionHandler(ClientHandler):
    def get_response(self, request):
        response = super(SessionHandler, self).get_response(request)
        response.session = request.session.copy()
        return response

class SessionTestCase(TestCase):
    def _pre_setup(self):
        super(SessionTestCase, self)._pre_setup()
        self.client.handler = SessionHandler()

class FooTestCase(SessionTestCase):
    def test_session_exists(self):
        resp = self.client.get("/")
        self.assert_(hasattr(resp, "session"))
        self.assert_("my_session_key" in resp.session)
        self.assertEqual(resp.session["my_session_key"], "Hello world!")