from django import forms
from mailclient.mmclient import getListOfLists

print "CALLING OS"

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MI.settings")

class SignUp(forms.Form):
	name = forms.CharField(label="Your Full Name", max_length=100, required=True)
	email = forms.EmailField(label="Email ID", required=True)
	pwd = forms.CharField(label="Password",widget=forms.PasswordInput, required=True)
	essay = forms.CharField(widget=forms.Textarea, max_length=800, required=True)	

class Login(forms.Form):
	username = forms.CharField(label="Username", required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

class Compose(forms.Form):
	email = forms.EmailField(label="Email ID", widget=forms.HiddenInput)
	# CHOICES = get list of all lists the user has subscribed to
	CHOICES = (('1','sample'),)
	#subscribed_lists, other_lists = getListOfLists(email)
	#for lst in subscribed_lists:
			# list name and list address
	#		CHOICES = CHOICES + ((lst[1],lst[0]),)
	print "CH",CHOICES
	recepient = forms.ChoiceField(choices=CHOICES)
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	

