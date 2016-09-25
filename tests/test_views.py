"""
Unit test for views.py
"""


from topmenu import views
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from topmenu.models import User, Listing


"""
from topmenu import views
from django.test.client import ClientHandler
from django.test.testcases import SimpleTestCase
"""
class BaseTest(TestCase):
	def setUp(self):
		self.url = reverse('topmenu:menu_2')
		self.c = Client()



class BadRequestArg(BaseTest):
	# best practices for creating bad request object?
	pass

class CorrectSMSSent(BaseTest):
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

	def test_MainMenu(self):
		"""NEEDS TO test that menu_2 creates a new user database entry when 
		required. Tests that 'active_urls' = TOP_MENU_URLS. Tests that for 
		both new and returning users, HttpResponse(status=200) is returned.
		"""

		# Precondition check verifies no users currently in test db.
		self.assertEqual(User.objects.count(), 0)

		# simulate incoming request
		self.c.post('/', {'From':'12345678901', 'Text':'1'})

		# why again is this needed?
		response = self.c.post(reverse('topmenu:menu_2'), kwargs={'From':'12345678901', 'Text':'1'})


		if create_user is not None:
			
			# Verify that db entry for new user was created
			self.assertEqual(User.objects.count(), 1)

			# self.assertEqual(self.client.session['active_urls'], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(response.status_code, 200)

		else:
			# self.assertEqual(self.client.session["active_urls"], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(response.status_code, 200)

class PostingSequenceTestCase(BaseTest):
	"""Tests for posting sequence."""

	def test_posting_smokes(self):
		# precondition check verifies that no users currently in test db:
		self.assertEqual(Listing.objects.count(), 0)
		# querry server and create session:
		self.c.post('/', {'From':'12345678901', 'Text':'1'})
		# select option 1, "For sale" listings:
		self.c.post('/', {'From':'12345678901', 'Text':'1'})
		# select option 5, "Post listing":
		self.c.post('/', {'From':'12345678901', 'Text':'5'})
		# submit listing subject:
		self.c.post('/', {'From':'12345678901', 'Text':'Smoke test subject'})
		# submit listing description:
		self.c.post('/', {'From':'12345678901', 'Text':'Smoke test description'})
		# select option 1 to confirm listing and commit to db:
		self.c.post('/', {'From':'12345678901', 'Text':'1'})
		# verify that listing entry was created:
		self.assertEqual(Listing.objects.count(), 1)

	def test_post_subject_request(self):
		pass

	def test_post_description_request(self):
		pass

	def test_post_review(self):
		pass

	def test_post_commit(self):
		pass
