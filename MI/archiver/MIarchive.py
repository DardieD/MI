from zope.interface import implementer
from mailman.interfaces.archiver import IArchiver

import email.utils
import time
from datetime import datetime
import uuid

from MI import models
from mailclient import mmclient

import logging
log = logging.getLogger('mailman.error')

@implementer(IArchiver)
class MIArchive:
    """This is the docstring."""

    name = 'MIArchive'

    @staticmethod
    def list_url(mlist):
        """See `IArchiver`."""
	raise NotImplemented 

    @staticmethod
    def permalink(mlist, msg):
        """See `IArchiver`."""
	raise NotImplemented

    @staticmethod
    def archive_message(mlist, message):
        """See `IArchiver`."""
        
	log.info("MI: Archive_message")
	print "\n\nWe got a new message"
	
	try:
		#Temporary variables used in this function
		msg_date=""
		msg_body = ""
		
		try:
			timestamp = time.mktime(email.utils.parsedate(message['Date']))
			msg_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
			# To get the body from multipart messages
			for part in message.walk():
				if part.get_content_type():
					msg_body = msg_body + part.get_payload(decode=True)
		except:
			msg_date = datetime.date.today().strftime('%Y-%m-%d')

		
		# Get the Screen-name of the ID corresponding to this author
		author_name=""
		author_email=""
		try:
			email_id = message['From']
			# If the email_id is of the form root<root@systers-dev.systers.org>, extract the actual emailid
			if '<' in email_id and '>' in email_id:
				pos1 = email_id.find('<')+1
				pos2 = email_id.find('>')
				email_id = email_id[pos1:pos2]
				
			author_email = email_id
			author_name = mmclient.getUserName(email_id)

		except Exception as ex:
			log.info("MI:Exception", ex)
			print ex
			author_name = email_id
					
		# If the message is a reply, generate threadid
		if 'In-Reply-To' in message.keys():
			# Implies is a reply
			# Get id of message replied to 
			# Get threadid of message replied to
			# Assign this thread id to current message
			replied_to = message['In-Reply-To']
			temp = models.MessageRenderer.objects.filter(msgid=replied_to)[0]
			log.info(temp.threadid)
			print "This was a reply to ->THREAD ID:", temp.threadid
			# Create MessageRenderer model object
			msg = models.MessageRenderer(subject=message['Subject'], email=author_email, author=author_name, date=msg_date,listname=mlist.fqdn_listname, msg=msg_body, msgid=message['Message-ID'], threadid=temp.threadid)
		else:
			log.info("ELSE")
			# Is a new message. Use message-id as thread-id 
			unique_id = message['Message-ID']
			msg = models.MessageRenderer(subject=message['Subject'], email=author_email, author=author_name, date=msg_date,listname=mlist.fqdn_listname, msg=msg_body, msgid=message['Message-ID'], threadid=unique_id)

		# Save to DB
		msg.save()
		log.info("MI: Message Saved")

	except Exception,ex:
		print "OOPS ! An error occured"
		print ex
		log.exception(ex)

