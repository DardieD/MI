import os, time, smtplib, subprocess
from mock import patch
from pickle import dumps
from sys import path

def t():	

	#var = "Currently available lists:" , client.lists
	print "Currently available lists: \r\n ", client.lists

	print "Currently available domains: \r\n ", client.domains

	#return var
	return "You are seeing this because client worked correctly"


# Add mailman.client to path if it doesn't already exist
MM_PATH = '/root/mailman.client/src/'
if not MM_PATH in path:
    path.append(MM_PATH)

#Create Client object
from mailmanclient import Client
client = Client('http://127.0.0.1:8001/3.0','restadmin','restpass')
