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


def getListOfLists(email):
	'''
	Get all available lists for a client
	'''
	#retreive user using email-id
	user = client.get_user(email)
	
	print '$$$$$$$$$$$$$ ATTRIBUTE TEST $$$$$$$$$$$$$$$$$$$$44'
	l = client.lists[0]
	print l
	s = l.settings
	print s['fqdn_listname']
	print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44'
	#return lists subscribed to using subscription_list_ids property
	return user.subscription_list_ids, client.lists
	
# Add mailman.client to path if it doesn't already exist
MM_PATH = '/root/mailman.client/src/'
if not MM_PATH in path:
    path.append(MM_PATH)

#Create Client object
from mailmanclient import Client
client = Client('http://127.0.0.1:8001/3.0','restadmin','restpass')

#temporary subscription code
'''
l1 = client.get_list('mi-one@smtp.gmail.com')
l2 = client.get_list('mi-three@smtp.gmail.com')

l1.subscribe('salunkeshanu91@gmail.com','Shanu')
l2.subscribe('salunkeshanu91@gmail.com','Shanu')
'''
