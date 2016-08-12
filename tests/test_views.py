"""
Unit test for views.py
"""

from topmenu import views
from django.test.client import ClientHandler
from django.test import TestCase

class BaseTest(TestCase):
	def __init__(self):
		self.url = reverse('topmenu:plivo_endpoint')

	def setUp(self):
		self.url = reverse('topmenu:plivo_endpoint')



class BadRequestArg(TestCase):
	# best practices for creating bad request object?
	pass

class CorrectSMSSent(TestCase):
	def test_post_subject_request(self):
		pass
	def test_post_description_request(self):
		pass
	def test_post_review(self):
		pass
	def test_post_commit(self):
		pass



class MainMenuUnitTests(BaseTest):
	"""Unit tests for the main menu (aka menu_2)"""

	def test_menu_2(self):
		"""NEEDS TO test that menu_2 creates a new user database entry when 
		required. Tests that 'active_urls' = TOP_MENU_URLS. Tests that for 
		both new and returning users, HttpResponse(status=200) is returned.
		"""
		# simulate incoming request
		c = ClientHandler()

		self.c.post(reverse('topmenu:menu_2'))

		# why again is this needed?
		response = self.c.post(reverse('topmenu:plivo_endpoint'), kwargs={'From':'12345678901', 'Text':'1'})


		if create_user is not None:
			# Precondition check verifies no users currently in test db.
			self.assertEqual(User.object.count(), 0)

			# Verify that db entry for new user was created
			self.assertEqual(User.object.count(), 1)

			# self.assertEqual(self.client.session['active_urls'], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(response.status_code, 200)

		else:
			# self.assertEqual(self.client.session["active_urls"], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(response.status_code, 200)

