"""
Unit test for views.py
"""

from topmenu import views
from django.test.client import ClientHandler
import unitttest

class BadRequestArg(unitttest.TestCase):
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

class DefaultDataHandledCorrectly(unitttest.TestCase):
	def test_post_description_request(self):
		"""Tests that following post_subject_request, 
		request.session['default_data'] == request.session['new_post_subject']
		"""

		self.assertEqual(request.session['new_post_subject'], request.session['default_data'])

	def test_post_review(self):
		"""Tests that following post_description_request, 
		request.session['default_data'] == request.session['new_post_description']
		"""

		self.assertEqual(request.session['new_post_description'], request.session['default_data'])

	def test_post_commit(self):
		"""
		
		"""

		if request.session['default_data'] == '1':
			self.assertEqual(Listing.objects.create(header=request.session['new_post_subject'], 
				detail=request.session['new_post_description'], category=category),
				Listing.objects.get(detail=request.session['new_post_description'])
			self.assertEqual(request.session['active_urls']['default_url'], reverse('topmenu:menu_2'))

		elif request.session['default_data'] == '9':
			



