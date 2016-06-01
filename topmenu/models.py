from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone

class Listing(models.Model):
	header = models.CharField(max_length = 40)
	#adding detail as an attribute of the same object instance:
	detail = models.CharField(max_length = 140)
	pub_date = models.DateTimeField('date posted')

	def __str__(self):
		return "%s, %s" % (self.header, self.detail)
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

class User_data(models.Model): # is serial id automatically pk?
	user_id = models.AutoField(primary_key = True)
	phone_num = models.PositiveIntegerField(max_length = 10)
	#user_carrier = models.PositiveIntegerField(max_length = 3) strategies to get this?
	user_jointime = models.DateTimeField() #need to read up on this
	user_state = models.PositiveIntegerField(max_length = 2)
	#user_loc = models.CharField() # read up on CharField parameters. this will eventually make it's own api call to map a radius
	user_sms_quant = models.PositiveIntegerField(max_length = 4)
	user_language = models.CharField(max_length = 20)

class SMS_data(models.Model):
	sms_id = models.AutoField(primary_key = True)
	messageuuid = models.CharField(max_length = 40)
	user_id = models.ForeignKey('User_data')
	source = models.PositiveIntegerField(max_length= 11)
	destination = models.PositiveIntegerField(max_length = 11)
	message_content = models.CharField(max_length = 140)
	# image_content = models.ImageField()
	message_time = DateTimeField(default = timezone.now) #this will auto populate or do i handle in views?




