class Message():

	def __init__(self,subject="HELLO",author="JD",date="01/01/01",listname="LIST:WELCOME",msg="The sky is blue",msgid="m001"):
		self.subject = subject
		self.author= author
		self.date= date
		self.listname= listname
		self.msg= msg
		self.msgid= msgid

	def getMessage():
		mssg = {'Subject':self.subject, 'Author':self.author,'Date':self.date, 'Listname':self.listname, 'Message':self.msg,'Message ID':self.msgid}
		return mssg
