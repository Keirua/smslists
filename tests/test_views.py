"""
Unit test for views.py
"""

from topmenu import views
from django.test.client import ClientHandler
import unitttest

class BadRequestArg(unitttest.TestCase):
	# best practices for creating bad request object?
	pass

class CorrectSMSSent(unitttest.TestCase):
	def test_post_subject_request(self):
		pass
	def test_post_description_request(self):
		pass
	def test_post_review(self):
		pass
	def test_post_commit(self):
		pass

class MainMenuUnitTests(unitttest.TestCase):
	"""Unit tests for the main menu (aka menu_2)"""

	def test_menu_2(self):
		"""NEEDS TO test that menu_2 creates a new user database entry when 
		required. Tests that 'active_urls' = TOP_MENU_URLS. Tests that for 
		both new and returning users, HttpResponse(status=200) is returned.
		"""

		self.assertEqual(phone_num, request.session["phone_num"])

		if create_user is not None:
			# figure out how to assert that new user is created
			self.assertEqual(request.session["active_urls"], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(menu_2(self.request), HttpResponse(status=200))

		else:
			self.assertEqual(request.session["active_urls"], views.menu_2.TOP_MENU_URLS)
			self.assertEqual(menu_2(self.request), HttpResponse(status=200))

class ListingsMenusUnitTests(unitttest.TestCase):
	"""Unit tests for listings menus."""

	def test_listings(self):
		"""
		"""
		self.assertIsInstance(displayed_items, views.listings)

		# how to write tests for for-loop?

		self.assertEqual(menu_2(self.request), HttpResponse(status=200))

	def test_listing_detail(self):
		pass

class PostCreationUnitTests(unitttest.TestCase):
	"""Unit tests for the post creation process."""

	def test_post_subject_request(self):
		"""Tests that 'active_urls' from previous views are cleared,
		tests that 'default_url' is mapped to 'topmenu:post_description_request',
		tests that view returns HttpResponse(status=200).
		"""

		self.assertEqual((request.session['active_urls'].clear()), None)
		self.assertEqual((request.session['active_urls']['default_url']), 
			(reverse('topmenu:post_description_request', kwargs={'category':category})))
		self.assertEqual(post_subject_request(self.request), 
			HttpResponse(status=200))

	def test_post_description_request(self):
		"""Tests that following post_subject_request, 
		request.session['default_data'] == request.session['new_post_subject'].
		Tests that post_description_request returns HttpResponse(status=200)
		"""

		if request.session['default_data'] == '9':
			self.assertNotIn(('default_url'), (request.session['active_urls']))
			self.assertNotIn(('default_data'), (request.session))
			self.assertNotIn(('new_post_subject'), (request.session))
			self.assertNotIn(('new_post_description'), (request.session))

		else: 
			self.assertEqual(request.session['new_post_subject'], request.session['default_data'])
			self.assertEqual(post_description_request(self.request), 
				HttpResponse(status=200))

	def test_post_review(self):
		"""Tests that following post_description_request, 
		request.session['default_data'] == request.session['new_post_description']
		"""

		if request.session['default_data'] == '9':
			self.assertNotIn(('default_url'), (request.session['active_urls']))
			self.assertNotIn(('default_data'), (request.session))
			self.assertNotIn(('new_post_subject'), (request.session))
			self.assertNotIn(('new_post_description'), (request.session))
		else:	
			self.assertEqual(request.session['new_post_description'], request.session['default_data'])
			self.assertEqual(request.session["active_urls"]["default_url"], 
				reverse("topmenu:post_commit", kwargs={'category':category}))
			self.assertEqual(post_review(self.request), 
				HttpResponse(status=200))


	def test_post_commit(self):
		"""Tests that if 'default_data' == '1', post subject and description 
		are committed. Tests that if 'default_data' == '9', 'default_url', 
		'default_data', 'new_post_subject' and 'new_post_description' are 
		deleted.
		"""

		if request.session['default_data'] == '1':
			self.assertEqual(Listing.objects.create(header=request.session['new_post_subject'], detail=request.session['new_post_description'], category=category), Listing.objects.get(detail=request.session['new_post_description'])
			self.assertEqual((request.session['active_urls']['default_url']), reverse('topmenu:menu_2'))
			self.assertEqual(post_commit(self.request), HttpResponse(status=200))

		elif request.session['default_data'] == '9':
			self.assertNotIn(('default_url'), (request.session['active_urls']))
			self.assertNotIn(('default_data'), (request.session))
			self.assertNotIn(('new_post_subject'), (request.session))
			self.assertNotIn(('new_post_description'), (request.session))
			self.assertEqual(post_commit(self.request), HttpResponse(status=200))

		else:
			self.assertEqual((request.session["active_urls"]["default_url"]), (reverse("topmenu:post_commit", 
				kwargs={'category':category}))
			self.assertEqual(post_commit(self.request), HttpResponse(status=200))
