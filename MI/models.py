from django.db import models

# Attempt at creating a model for each message

class MessageRenderer(models.Model):
	subject = models.CharField(max_length=50)
	author = models.CharField(max_length=20)
	date = models.CharField(max_length=10)
	listname = models.CharField(max_length=20)
	msg = models.CharField(max_length=500)
	msgid = models.CharField(max_length=5)
