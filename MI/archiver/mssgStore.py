from sys import path
from email import message_from_string

MM_path = "/root/mailman/src/"
if MM_path not in path:
	path.append(MM_path)
	#print path

from mailman.interfaces.messages import IMessageStore
from zope.component import getUtility

ob = IMessageStore()
#Initial registration of utility
from zope.component import getGlobalSiteManager
getGlobalSiteManager().registerUtility(ob,IMessageStore)
message_store = getUtility(IMessageStore)


msg = message_from_string("""\
... Subject: An important message
...
... This message is very important.
... """)
msg['Message-ID']='<87myycy5eh.fsf@uwakimon.sk.tsukuba.ac.jp>'
message_store.add(msg)
print msg.as_string()

print "Done"
