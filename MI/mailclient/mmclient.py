import os, time, smtplib, subprocess
from mock import patch
from pickle import dumps
from sys import path

from django.contrib.auth.models import User

import logging
log = logging.getLogger('mailman.error')

def createUser(username, email, password):
	'''
	Create New user in the mailman system 
	IF the user doesn't already exist 
	'''
	try:
		client.get_user(email)
		
	except Exception as ex:
		log.info("USER DOESNT EXIST IN MM, CREATE")
		client.create_user(email=email, password=password, display_name=username)

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
	try:
		user = client.get_user(email)
		return user.preferences
		
	except Exception as ex:
		log.error("USER NOT FOUND:", ex)
		#Fall Back to Global Preferences
		return client.preferences
		
def setUserPreferences(email, prefs):
	'''
	return dictionary of user's preferences
	'''
	try:
		user = client.get_user(email)
		original_prefs = user.preferences
		print user
		user.preferences['acknowledge_posts'] = prefs['acknowledge_posts']
		user.preferences['delivery_mode'] = prefs['delivery_mode']
		user.preferences['delivery_status'] = prefs['delivery_status']
		user.preferences['hide_address'] = prefs['hide_address']
		user.preferences['preferred_language'] = prefs['preferred_language']
		user.preferences['receive_list_copy'] = prefs['receive_list_copy']
		user.preferences['receive_own_postings'] = prefs['receive_own_postings']
		
		user.save()
		return "Preferences Changed Successfully"
		
	except Exception as ex:
		log.error("UNABLE TO CHANGE PREFERENCES:",ex)
		#Fall Back to Global Preferences
		return "An Error Occured in mmclient:setUserPreferences ", ex
		

def getProfileDetails(email):
	'''
	Return dictionary of user profile details as a list of display_name,email elements
	The first name-email pair belongs to user.display_name and the id used to create the object
	Subsequent elements are derived from user.addresses 
	'''
	try:
		user = client.get_user(email)
		name_email_list = {'display_name':user.display_name,'email':email}
		return name_email_list
		
	except Exception as ex:
		return {'display_name':'ERROR', 'email':'ERROR'}


	
def setProfileDetails(email, profile_details):
	'''
	Set the profile name provided as a dictionary
	'''
	try:

		user = client.get_user(email)
		#Bandaid cure for making profile changes stick
		print user
		old_name = user.display_name
		user.display_name = profile_details['display_name']
		user.save()
		return "Profile Details Successfully Set"			
	except Exception as ex:
		return "An error occured in mmclient: ", ex
			
def changePwd(email, pwd):
	'''
	Change the user's password
	both in mailman
	and in the system
	'''
	try:
		#Changin password in mm system
		user = client.get_user(email)
		#Bandaid cure for making profile changes stick
		print user
		user.password = pwd
		user.save()
		
		#Changing password in MI
		u = User.objects.get(email__exact=email)
		u.set_password(pwd)
		u.save()
		return "Your password was successfully changed"	
			
	except Exception as ex:
		return "An error occured in mmclient:changePwd ", ex

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
		return True
	except Exception as ex:
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
		lst.unsubscribe(email)
		return True
	except Exception as ex:
		return False

#Create Client object
from mailmanclient import Client
from config import config

client_details = config.getRestConfig()
client = Client(client_details[0],client_details[1],client_details[2])

