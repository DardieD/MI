from MI import models
from MI.mailclient import mmclient


def getLatestMessages(email, n=10):
	'''
	Get the latest (last n) messages to the lists
	subscribed to by user with email = email
	'''
	try:
		subscribed_lists, other_lists = mmclient.getListOfLists(email)
		subscribed_lists = [row[1] for row in subscribed_lists]
	except:
		return []
	message_list = models.MessageRenderer.objects.filter(listname__in=subscribed_lists).order_by('pk').reverse()[:n]
	
	print len(message_list)
	return message_list

def getMessagesByList(list_of_lists, n=10):
	'''
	Get the last n messages from matching list(s)
	'''
	message_list = models.MessageRenderer.objects.filter(listname__in=subscribed_lists).order_by('pk').reverse()[:n]
	return message_list

def getMessageByThreadID(threadid):
	'''
	Get all messages with a given threadid
	'''
	message_list = models.MessageRenderer.objects.filter(threadid=threadid).order_by('pk')
	print "Message List generated for threadid ", threadid 
	print "Message List length: ", len(message_list)
	return message_list
	
def getMessagesByDate():
	'''
	'''
	return []
	
def getMessagesByAuthor():
	'''
	'''
	return []
	

'''
from sys import path
pth = "/vagrant/MI/"
if pth not in path:
	path.append(pth)
# To test 
mym = MessageRender()
mym.getLatestMessages("root@systers-dev.systers.org")
mym.getLatestMessages('salunkeshanu91@gmail.com')
'''
