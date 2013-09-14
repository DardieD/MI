from MI import models
from MI.mailclient import mmclient
from django.db.models import F

import MessageRenderer

def inFavorites(user, msgid):
	'''
	Check whether this message is
	Already added in the favoties list 
	'''
	msg_list = user.messages.filter(msgid__exact=msgid)
	
	if not msg_list:
		return False
	else:
		return True

def addToFavorites(email, msgid):
	'''
	Check whether user with given email
	exists in the Favorite's model
	i.e user need not be created
	'''
	try:
		try:
			user = models.Favorites.objects.get(email__exact=email)
		except:
			print "USER HAS NOT YET BEEN ADDED TO FAVORITES LIST"
			user = models.Favorites(email=email)
			user.save()
	
		print "In Favorites", inFavorites(user, msgid)
		#Get MIMessage object
		if not inFavorites(user, msgid):
			msg = MessageRenderer.getMessageByMessageID(msgid)
			user.messages.add(msg)	
	
		return "Message Added To Favorites List"
		
	except Exception as ex:
		print ex
		return ex

def removeFromFavorites(email, msgid):
	'''
	Remove a message from the favorites list
	'''
	print "Remove from Favorites"
	
	try:
		user = models.Favorites.objects.get(email__exact=email)
		print type(user), msgid
		
		print "In Favorites", inFavorites(user, msgid)
		#Only attempt removal if message already exists in favorites
		if inFavorites(user, msgid):
			msg = MessageRenderer.getMessageByMessageID(msgid)
			user.messages.remove(msg)
				
		return "Message Removed From Favorites List"
		
	except Exception as ex:
		print ex
		return ex


def getFavorites(email):
	'''
	Returns QuerySet of all messages
	in user's favorite list
	'''
	try:
		user = models.Favorites.objects.get(email__exact=email)
		return user.messages.all()
	except Exception as ex:
		#The user never registered favorites
		return 
	
	
	
	
