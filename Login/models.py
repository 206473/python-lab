from django.db import models
from django import forms
class User(models.Model):
	login = models.CharField('login',max_length=30, default='')
	password = models.CharField('password',max_length=30, default='')
	email = models.EmailField('Email',blank=True, default='')
	def __str__(self):
		return '%s' % (self.login)

