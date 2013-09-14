from django import forms
from mailclient.mmclient import getListOfLists
from django.forms import extras

from validators import validators

class SignUp(forms.Form):
	name = forms.CharField(label="Username", max_length=100, required=True)
	email = forms.EmailField(label="Email ID", required=True, validators=[validators.validate_email_unique])
	pwd = forms.CharField(label="Password",widget=forms.PasswordInput, required=True)
	essay = forms.CharField(widget=forms.Textarea, max_length=800, required=True)	

class Login(forms.Form):
	username = forms.CharField(label="Username", required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

class Profile(forms.Form):
	'''
	def __init__(self, profile_details, *args, **kwargs):
		super(Profile, self).__init__(*args, **kwargs)
		
		for i,pair in enumerate(profile_details):
			d_name = "display_name" + str(i)
			e_name = "email" + str(i)
			self.fields[d_name] = forms.CharField(label="Name", required=False, initial= pair['display_name'])
			self.fields[e_name] = forms.EmailField(label="Email ID", required=False, initial=pair['email'])
        	
        	
        	self.fields['display_name'] = forms.CharField(label="Name", required=False, initial= profile_details['display_name'])
        	self.fields['email'] = forms.EmailField(label="Email ID", required=False, initial=profile_details['email'])
	'''
	display_name = forms.CharField(label="Screen Name", max_length=100, required=True)
	#email = forms.EmailField(label="Email ID", required=True)
	
class ChangePwd(forms.Form):
	'''
	Changing Password
	'''
	old_pwd = forms.CharField(widget=forms.PasswordInput(), label="Old Password")
	new_pwd = forms.CharField(widget=forms.PasswordInput(),label="New Password")
	new_pwd_again = forms.CharField(widget=forms.PasswordInput(),label="New Password(again)")
	
class Preferences(forms.Form):
	'''
	Form to render the User Preferences
	'''		
	
	TF = (('false', 'False',), ('true', 'True',))
	DELMODE = (('regular','regular',),('digest','digest',))
	DELSTAT = (('enabled','enabled',),('disabled','disabled',))
	LANGS =  (('en','en',),('ja','ja',))
	
	acknowledge_posts = forms.ChoiceField(widget=forms.RadioSelect, choices=TF)
	delivery_mode = forms.ChoiceField(widget=forms.RadioSelect, choices=DELMODE)
	delivery_status = forms.ChoiceField(widget=forms.RadioSelect, choices=DELSTAT)
	hide_address = forms.ChoiceField(widget=forms.RadioSelect, choices=TF)
	preferred_language = forms.ChoiceField(widget=forms.RadioSelect, choices=LANGS)
	receive_list_copy = forms.ChoiceField(widget=forms.RadioSelect, choices=TF)
	receive_own_postings = forms.ChoiceField(widget=forms.RadioSelect, choices=TF)

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
	
	
	
	
	
	
	
	
	
	
	
	

