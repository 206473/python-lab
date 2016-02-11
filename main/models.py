from django.db import models
from Login.models import User
from django import forms

class Subscriptions(models.Model):
	url = models.CharField('url',max_length=255, default='')
	user = models.ManyToManyField(User)
	def __str__(self):
		return '%s' % (self.url)
class Images(models.Model):
	subscribe_id = models.IntegerField('subscribe_id')
	url = models.CharField('url',max_length=255, default='')
	def __str__(self):
		return '%s' % (url)