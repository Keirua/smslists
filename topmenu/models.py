from __future__ import unicode_literals

from django.db import models

class Question(models.Model): #what does models.Model indicate?
	question_text = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('date posted')
	