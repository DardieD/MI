import os, time, smtplib, subprocess
from mock import patch
from pickle import dumps
from sys import path

def getUserPreferences(email):
	'''
	return dictionary of user's preferences
	'''
	user = client.get_user(email)
	return user.preferences

def getListOfLists(email):
	'''
	Get all available lists for a client
	'''
	try:
		#retreive user using email-id
		user = client.get_user(email)
	except Exception:
		return [], client.lists

	# list_ids of lists subscribed by user 
	subscribed_list_ids = user.subscription_list_ids

	# all available lists
	all_lists = client.lists

	# compare to get other lists (those not subscribed to)
	other_lists = []
	subscribed_lists = []

	for item in all_lists:
		if item.list_id not in subscribed_list_ids:
			other_lists.append([item.list_name, item.fqdn_listname])
		else:
			subscribed_lists.append([item.list_name, item.fqdn_listname])

	return subscribed_lists, other_lists

def subscribe(email , fqdn_listname):
	'''
	subscribe user with email = email to list with fqdn_listname=fqdn_listname
	'''
	try:
		#retreive user using email-id
		user = client.get_user(email)
		lst = client.get_list(fqdn_listname)
		lst.subscribe(email, user.display_name)
		return True
	except Exception:
		return False
	
def unsubscribe(email , fqdn_listname):
	'''
	subscribe user with email = email to list with fqdn_listname=fqdn_listname
	'''
	try:
		#retreive user using email-id
		user = client.get_user(email)
		print "USER", user
		print "FQDN", fqdn_listname
		lst = client.get_list(fqdn_listname)
		print "LST", lst
		lst.unsubscribe(email)
		return True
	except Exception:
		return False

# Add mailman.client to path if it doesn't already exist
MM_PATH = '/root/mailman.client/src/'
if not MM_PATH in path:
    path.append(MM_PATH)

#Create Client object
from mailmanclient import Client
client = Client('http://127.0.0.1:8001/3.0','restadmin','restpass')

