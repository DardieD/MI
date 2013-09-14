import ConfigParser
import os

def getRestConfig():
	'''
	Get the resturl, admin and password from the configuration file
	'''
	#Create configparser object
	config = ConfigParser.ConfigParser()
	p= os.path.join(os.path.dirname(__file__),'config.cfg')
	
	config.read(p)
	config.sections()
	url = config.get('mailmanclient','resturl')
	admin = config.get('mailmanclient','restadmin')
	pwd = config.get('mailmanclient','restpass')
	
	return [url,admin,pwd]
