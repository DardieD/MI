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

class MessageRenderer(models.Model):
	subject = models.CharField(max_length=100)
	author = models.EmailField(max_length=100)
	date = models.DateField()
	listname = models.CharField(max_length=50)
	msg = models.TextField()
	msgid = models.CharField(max_length=100)
	threadid = models.CharField(max_length = 10, unique=False) 
	

	def __unicode__(self):
		return u"%s \n %s\n %s\n %s\n %s\n %s" % (self.subject, self.author, self.date, self.listname, self.msg, self.msgid)

		
