from django import forms

class SignUp(forms.Form):
	subject = forms.CharField(label="Your Full Name", max_length=100, required=True)
	sender = forms.EmailField(label="Email ID", required=True)
	essay = forms.CharField(widget=forms.Textarea, max_length=800, required=True)	

class Login(forms.Form):
	username = forms.CharField(label="Username", required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

class Compose(forms.Form):
	# CHOICES = get list of all lists the user has subscribed to
	CHOICES = (('1','Dev-list'),('2','Request'),('3','SampleList3'))
	recepient = forms.ChoiceField(choices=CHOICES)
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	
