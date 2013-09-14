'''
from sys import path
p = "/vagrant/MI/"
if p not in path:
	path.append(p)
'''
import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MI.settings")

from django.db import models
import uuid

class MIMessage(models.Model):
	'''
	Model for messages in the database
	'''
	subject = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	date = models.DateField()
	listname = models.CharField(max_length=50)
	msg = models.TextField()
	msgid = models.CharField(max_length=100)
	threadid = models.CharField(max_length = 10, unique=False) 
	

	def __unicode__(self):
		return u"%s \n %s\n %s\n %s\n %s\n %s" % (self.subject, self.author, self.date, self.listname, self.msg, self.msgid)

class Favourites(models.Model):
	'''
	Model for favourites mapped many-many using 
	user's email id
	'''
	email = models.EmailField(max_length=100)
	messages =  models.ManyToManyField(MIMessage)
	
	def __unicode__(self):
	        return self.messages

		

	
	
