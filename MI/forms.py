from django import forms
from mailclient.mmclient import getListOfLists
from django.forms import extras

class SignUp(forms.Form):
	name = forms.CharField(label="Username", max_length=100, required=True)
	email = forms.EmailField(label="Email ID", required=True)
	pwd = forms.CharField(label="Password",widget=forms.PasswordInput, required=True)
	essay = forms.CharField(widget=forms.Textarea, max_length=800, required=True)	

class Login(forms.Form):
	username = forms.CharField(label="Username", required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

class Profile(forms.Form):

	def __init__(self, profile_details, *args, **kwargs):
		super(Profile, self).__init__(*args, **kwargs)
		print "##########################################"
		print profile_details
		for i,pair in enumerate(profile_details):
			d_name = "display_name" + str(i)
			e_name = "email" + str(i)
			self.fields[d_name] = forms.CharField(label="Name", required=False, initial= pair['display_name'])
			self.fields[e_name] = forms.EmailField(label="Email ID", required=False, initial=pair['email'])
        	#self.fields.keyOrder = ['recipient', 'subject', 'message']
        	
	#display_name = forms.CharField(label="Name", required=False)
	#email = forms.EmailField(label="Email ID", required=False)

class Compose(forms.Form):

	def __init__(self, email, *args, **kwargs):
		super(Compose, self).__init__(*args, **kwargs)
		
		subscribed_lists, other_lists = getListOfLists(email)
		CHOICES = ()
		for lst in subscribed_lists:
			#list name and list address
			CHOICES = CHOICES + ((lst[1],lst[0]),)
		self.fields['recipient'] = forms.ChoiceField(choices=CHOICES)
        	self.fields.keyOrder = ['recipient', 'subject', 'message']
        
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	
class ArchiveRenderer(forms.Form):
	'''
	This form gets query parameters like listname and to-from dates
	to render the archive messages
	'''
	
	def __init__(self, email, *args, **kwargs):
		super(ArchiveRenderer, self).__init__(*args, **kwargs)
	
		subscribed_lists, other_lists = getListOfLists(email)
		CHOICES = ()
		for lst in subscribed_lists:
			#list name and list address
			CHOICES = CHOICES + ((lst[1],lst[0]),)
		
		self.fields['listnames'] = forms.ChoiceField(choices=CHOICES)
		self.fields.keyOrder = ['listnames', 'from_date', 'to_date']#,'order_by']
        
        #order_CHOICES = ()
	from_date = forms.DateField(widget=extras.SelectDateWidget)
	to_date = forms.DateField(widget=extras.SelectDateWidget)
	
	
	
	
	
	
	
	
	
	
	
	

