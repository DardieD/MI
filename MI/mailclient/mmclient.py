import os, time, smtplib, subprocess
from mock import patch
from pickle import dumps
from sys import path

import logging
log = logging.getLogger('mailman.error')

def getUserName(email):
	'''
	Get the user's display name for this email id
	'''
	try:
		user = client.get_user(email)
		return user.display_name
	except Exception as ex:
		log.error(ex)
		return email.split('@')[0]
	
def getUserPreferences(email):
	'''
	return dictionary of user's preferences
	'''
	user = client.get_user(email)
	return user.preferences

def getProfileDetails(email):
	'''
	return dictionary of user profile details as a list of display_name,email elements
	The first name-email pair belongs to user.display_name and the id used to create the object
	Subsequent elements are derived from user.addresses 
	'''
	try:
		#print "THE EMAIL IS", email
		name_email_list = []
		user = client.get_user(email)
		name_email_list.append({'display_name':user.display_name,'email':email})
		for address in user.addresses:
			#print type(address), type(email), address==email
			temp = address._address['email']
			print temp
			if  temp == email and address.display_name != user.display_name:
				#To deal with multiple dispaly names for same email id
				# Trying to set the display_name gives an AttributeError !
				#address.display_name = user.display_name
				pass
			else:
				# Multiple email ids
				name_email_list.append({'display_name':address.display_name,'email':address})
		return name_email_list
		
	except Exception as ex:
		print ex
		#log.error("MMClient getProfileDetails: Client doesn't exist")
		return []
	
def getListOfLists(email):
	'''
	Get all available lists for a client
	'''
	try:
		#retreive user using email-id
		user = client.get_user(email)
	except Exception:
		#User not listed with mmclient. 
		#Show all lists (Subscribed list is empty)
		#Add user to MM
		
		
		other_lists = []
		all_lists = client.lists
		for item in all_lists:
			other_lists.append([item.list_name, item.fqdn_listname])
		return [], other_lists

	# list_ids of lists subscribed by user 
	subscribed_list_ids = user.subscription_list_ids

	# all available lists
	all_lists = client.lists

	# compare to get other lists (those not subscribed to)
	other_lists = []
	subscribed_lists = []

	for item in all_lists:
		if item.list_id not in subscribed_list_ids:
			desc = item.settings['description']
			other_lists.append([item.list_name, item.fqdn_listname, desc])
		else:
			desc = item.settings['description']
			subscribed_lists.append([item.list_name, item.fqdn_listname, desc ])

	return subscribed_lists, other_lists

def subscribe(email , fqdn_listname):
	'''
	subscribe user with email = email to list with fqdn_listname=fqdn_listname
	'''
	log.info("SUBSCRIBING TO LIST", fqdn_listname)
	try:
		#retreive user using email-id
		user = client.get_user(email)
		lst = client.get_list(fqdn_listname)
		lst.subscribe(email, user.display_name)
		print "SUBSCRIBERS:", lst.members
		return True
	except Exception as ex:
		print ex
		return False
	
def unsubscribe(email , fqdn_listname):
	'''
	subscribe user with email = email to list with fqdn_listname=fqdn_listname
	'''
	log.info("UNSUBSCRIBING FROM LIST", fqdn_listname)
	try:
		#retreive user using email-id
		user = client.get_user(email)
		lst = client.get_list(fqdn_listname)
		print "SUBSCRIBERS:", lst.members
		lst.unsubscribe(email)
		return True
	except Exception as ex:
		print ex
		return False

# Add mailman.client to path if it doesn't already exist
MM_PATH = '/root/mailman.client/src/'
if not MM_PATH in path:
    path.append(MM_PATH)

#Create Client object
from mailmanclient import Client
client = Client('http://127.0.0.1:8001/3.0','restadmin','restpass')

