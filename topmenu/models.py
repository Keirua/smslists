from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone

class Listing(models.Model):
	listing_text = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('date posted')

	def __str__(self):
		return self.listing_text
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

class Listing_detail(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	ld_text = models.CharField(max_length=200)
	def __str__(self):
		return self.choice_text
	