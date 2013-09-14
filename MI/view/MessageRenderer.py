from MI import models
from MI.mailclient import mmclient
from django.db.models import F

def updateScreenname(old_name, new_name):
	'''
	Change all occurances of author to 
	New_Name in the database
	'''
	msg = models.MIMessage.objects.filter(author=old_name).update(author=new_name)
	return msg

def getLatestMessages(email, n=10):
	'''
	Get the latest (last n) messages to the lists
	subscribed to by user with email = email
	'''
	try:
		subscribed_lists, other_lists = mmclient.getListOfLists(email)
		subscribed_lists = [row[1] for row in subscribed_lists]
	except Exception as ex:
		print ex
		return []
	message_list = models.MIMessage.objects.filter(listname__in=subscribed_lists).order_by('pk').reverse()[:n]
	
	print len(message_list)
	return message_list

def getMessagesByList(list_of_lists, n=10):
	'''
	Returns QuerySet of the last n messages from matching list(s)
	'''
	message_list = models.MIMessage.objects.filter(listname__in=list_of_lists).order_by('pk').reverse()[:n]
	
	return message_list

def getMessageByThreadID(threadid):
	'''
	Returns QuerySet of messages with a given threadid
	'''
	message_list = models.MIMessage.objects.filter(threadid=threadid).order_by('pk')
	print "Message List generated for threadid ", threadid 
	print "Message List length: ", len(message_list)
	return message_list

def getMessageByMessageID(msgid):
	'''
	Return MIMessage object of message with
	given msgid
	'''
	message = models.MIMessage.objects.get(msgid=msgid)
	return message
		
def getMessagesBasicAchive(listname, from_date,to_date):
	'''
	Returns QuerySet of messages for given listname within date range
	Only display first message in thread ( where msgid = threadid )
	Basic Archives Display
	'''
	message_list = models.MIMessage.objects.filter(listname=listname).filter(date__range=[from_date, to_date]).filter(msgid=F('threadid')).order_by('-pk')
	return message_list


