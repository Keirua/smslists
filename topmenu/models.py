from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser

class User(DjangoUser):
	phone_num = models.BigIntegerField(max_length=10)
	# attempting to debug "integrity error, auth_user_username_key already exists"
	# DjangoUser.username = models.BigIntegerField(default=phone_num)
	#user_carrier = models.PositiveIntegerField(max_length = 3)
	user_jointime = models.DateTimeField(auto_now_add=True)
	user_loc = models.CharField(max_length=20) # read up on CharField parameters. this will eventually make it's own api call to map a radius
	user_sms_quant = models.PositiveIntegerField(max_length=4, default=1)
	user_language = models.CharField(max_length=20, default='English')

	def save(self, *args, **kwargs):
		self.username = str(self.phone_num)
		super(User, self).save(*args, **kwargs)

class Listing(models.Model):
	header = models.CharField(max_length=40)
	#adding detail as an attribute of the same object instance:
	detail = models.CharField(max_length=140)
	pub_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User)
	category = models.CharField(max_length=40)

	def __str__(self):
		return "%s, %s" % (self.header, self.detail)
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class SMS(models.Model):
	message_uuid = models.CharField(max_length=40)
	user = models.ForeignKey(User)
	source = models.PositiveIntegerField(max_length=11)
	destination = models.PositiveIntegerField(max_length =11)
	message_content = models.CharField(max_length=140)
	# image_content = models.ImageField()
	message_time = models.DateTimeField(auto_now_add= True) 




