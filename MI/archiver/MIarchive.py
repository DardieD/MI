from zope.interface import implementer
from mailman.interfaces.archiver import IArchiver

# To prevent django.core.exceptions.ImproperlyConfigured
#from django.conf import settings
#if not settings.configured:
#    settings.configure()

from sys import path
model_path="/vagrant/MI/"
if model_path not in path:
	path.append(model_path)

from MI import models

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
	log.info("MI ARCHIVER CALLED")

	print "Hello"

	try:
		print "Incoming Message"

		#try:
		#	settings.configure()
		#except Exception,ex:
		#	print "Settings already configured"
		#	log.exception(ex)

		msg = models.MessageRenderer(subject=message['Subject'], author=message['From'], date='1999-01-01',listname=mlist.fqdn_listname, msg=message.get_payload(), msgid=message['Message-ID'])
		msg.save()

	except Exception,ex:
		print "An error occured"
		log.exception(ex)
	'''
	try:
		print mlist.fqdn_listname
		print "TO:",message['To'],"FROM:",message['From'],"SUBJECT:",message['Subject']
		print message.get_payload() 
		#print "\n\n\n", message.as_string()
		#print "\n\n\n", message.__str__()

	except:
		print "An error occurred"
	'''
	log.info("MI MESSAGE SAVED")

