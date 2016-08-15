"""
Unit test for views.py
"""


from topmenu import views
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from topmenu.models import User


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

	def test_menu_2(self):
		"""NEEDS TO test that menu_2 creates a new user database entry when 
		required. Tests that 'active_urls' = TOP_MENU_URLS. Tests that for 
		both new and returning users, HttpResponse(status=200) is returned.
		"""

		# Precondition check verifies no users currently in test db.
		self.assertEqual(User.objects.count(), 0)

		# simulate incoming request
		self.c.post(reverse('topmenu:menu_2'))
		self.c.session['phone_num'] = '12345678901'

		# why again is this needed?
		response = self.c.post(reverse('topmenu:menu_2'), kwargs={'from':'12345678901', 'text':'1'})


		if create_user is not None:
			
			# Verify that db entry for new user was created
			self.assertEqual(User.objects.count(), 1)

			# self.assertEqual(self.client.session['active_urls'], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(response.status_code, 200)

		else:
			# self.assertEqual(self.client.session["active_urls"], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(response.status_code, 200)

