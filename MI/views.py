from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail

from mailclient import mmclient
from Message import Message
from MI import models

def welcome(request):
	'''
	View for welcome screen 
	'''
	# If form is already submitted
	if request.method == 'POST' or request.method =='GET': 
		form = forms.Login(request.POST)
		if form.is_valid(): 
			# Process the data in form.cleaned_data
			#responseurl = '/home/' + form.cleaned_data['username'] + '/' ; 
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				# Correct password, and the user is marked "active"
				auth.login(request, user)
				# Redirect to a success page.
				return HttpResponseRedirect("/home/")
			else:
				# Show an error page
				return HttpResponseRedirect("/")
	else:
        	form = forms.Login() # An unbound form

	return render_to_response('welcome.html', {'form': form}, context_instance=RequestContext(request))

def home(request):
	'''
	View for User's Home Page
	Authenticaltion required
	'''
	if request.user.is_authenticated():
		# Filer messages for user 
		mslist = models.MessageRenderer.objects.all()

		return render_to_response('home.html', {'mslist':mslist}, context_instance=RequestContext(request))

	else:
		return render_to_response('welcome.html',context_instance=RequestContext(request))
	
def compose(request):
	'''
	View for the compose screen
	Add parameters to take subject and recepients list
	in case of 'reply'
	'''
	#To be added: compose/new and compose/reply

	# If form is already submitted

	if request.method == 'POST': 
		print "form already sent"

		form = forms.Compose(request.POST)
		if form.is_valid(): 
			print "Sending email", send_mail('Test Subject', 'Here is the message.','root@systers-dev.systers.org',['test@systers-dev.systers.org'], fail_silently=False)
			
			return HttpResponseRedirect('/home/')
	else:
		subscribed_lists, other_lists = mmclient.getListOfLists(request.user.email)
		choices = ()
		for lst in subscribed_lists:
			# list name and list address
			choices = choices + ((lst[1],lst[0]),)
		#print "choices", choices
		data = {'CHOICES':choices,'email':request.user.email,'subject':'Random ','message':' Random'}
		#print "binding data"
        	form = forms.Compose(data) # An unbound form
		
	return render_to_response('compose.html', {'form': form}, context_instance=RequestContext(request))


def archives(request):
	'''
	View for the archives
	'''
	return render_to_response('archives.html')

def lists(request):
	'''
	View for rendering all available lists
	'''

	subscribed_lists, other_lists = mmclient.getListOfLists(request.user.email)
	return render_to_response('lists.html', {'subscribed_lists':subscribed_lists, 'other_lists':other_lists}, context_instance=RequestContext(request))

def newuser(request):
	'''
	View for New User Sign Up Sheet
	'''
	if request.method == 'POST': 
		form = forms.SignUp(request.POST)
		if form.is_valid(): 
		    	# Process the data in form.cleaned_data
			name = request.POST.get('name', '')
			pwd = request.POST.get('pwd', '')
			email = request.POST.get('email', '')
			essay = request.POST.get('essay', '')

			#Call sys-mailman signup module ?
			user = User.objects.create_user(username=name,email=email,password=pwd)
			user.save()

			return HttpResponseRedirect('/thanks/')
	else:
        	form = forms.SignUp() # An unbound form

	return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))

def thanks(request):
	'''
	View for User Profile
	'''
	return render_to_response('welcome.html',context_instance=RequestContext(request))

def profile(request):
	'''
	View for User Profile
	'''
	return render_to_response('profile.html')

def preferences(request):
	'''
	Show and edit user preferences
	'''
	prefs = mmclient.getUserPreferences(request.user.email)
	return render_to_response('preferences.html', {'prefs': prefs}, context_instance=RequestContext(request))

def logout(request):
	'''
	View for user logout
	'''
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")

def subscribe(request, fqdn_listname):
	''' 
	Subscribe to list with fqdn_listname = fqdn_listname
	'''
	success = mmclient.subscribe(request.user.email, fqdn_listname)
	return HttpResponseRedirect("/lists")

def unsubscribe(request, fqdn_listname):
	''' 
	Subscribe to list with fqdn_listname=fqdn_listname
	'''
	success = mmclient.unsubscribe(request.user.email, fqdn_listname)
	return HttpResponseRedirect("/lists")

