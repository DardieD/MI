from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from mailclient import mmclient
from Message import Message
from MI import models
from MI.view import MessageRender

from sqlite3 import IntegrityError

import urllib, hashlib

def welcome(request):
	'''
	View for welcome screen
	Welcome is a public screen that shows static information 
	that may be displayed as well as the login and signup forms. 
	'''
	# LOGIN Form
	# If login form is already submitted
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
        	form = forms.Login() # An unbound login form

	return render_to_response('welcome.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def home(request):
	'''
	View for User's Home Page
	'''
	
	if request.user.is_authenticated():
		# Filter messages for user 
		mslist = MessageRender.getLatestMessages(request.user.email)
		return render_to_response('home.html', {'mslist':mslist}, context_instance=RequestContext(request))
	else:
		return render_to_response('welcome.html',context_instance=RequestContext(request))

@login_required
def conversation(request, threadid):
	'''
	To View a conversation given the threadid
	'''
	
	if request.user.is_authenticated():
		# Get all messages in the conversation
		mslist = MessageRender.getMessageByThreadID(threadid)
		return render_to_response('view_conversation.html', {'mslist':mslist}, context_instance=RequestContext(request))
	else:
		return render_to_response('welcome.html',context_instance=RequestContext(request))

@login_required #(redirect_field_name='welcome')
def compose(request):
	'''
	View for the compose screen
	'''
	# If form is already submitted

	if request.method == 'POST': 
		form = forms.Compose(request.user.email, request.POST)
		if form.is_valid(): 
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = request.user.email
			recipient = []
			recipient.append(form.cleaned_data['recipient'])			
			send_mail(subject,message,sender,recipient, fail_silently=False)
			return HttpResponseRedirect('/home/')
	else:
        	form = forms.Compose(request.user.email) # An unbound form
	
	return render_to_response('compose.html', {'form': form}, context_instance=RequestContext(request))
	
	
@login_required
def reply(request, subject, msgid, rec):
	'''
	View for the Reply screen
	Replying to message with subject and msgid given 
	Recipient is the rec list
	'''
	# If form is already submitted
	if request.method == 'POST': 
		form = forms.Compose(request.POST)
		if form.is_valid(): 
			message = form.cleaned_data['message']
			sender = request.user.email
			recipient = []
			recipient.append(rec)
			send_mail(subject,message,sender,recipient,  headers = {'In-Reply-To': msgid} ,fail_silently=False)
			return HttpResponseRedirect('/home/')
	else:
        	form = forms.Compose(request.user.email) # An unbound form
		
	return render_to_response('compose.html', {'form': form}, context_instance=RequestContext(request))
	
	
	

@login_required 
def reply(request):
	'''
	Send reply email with In-Reply-To rmsid
	'''
	if request.method == 'POST': 
		form = forms.Compose(request.user.email, request.POST)
		if form.is_valid(): 
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = request.user.email
			print "Sending email", send_mail(subject,message,'root@systers-dev.systers.org',['test@systers-dev.systers.org'], fail_silently=False)
			
			return HttpResponseRedirect('/home/')
	else:
        	form = forms.Compose(request.user.email) # An unbound form
		
	return render_to_response('compose.html', {'form': form}, context_instance=RequestContext(request))


def archives(request):
	'''
	View for the archives
	'''
	return render_to_response('archives.html')


@login_required
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
			try:
				user = User.objects.create_user(username=name,email=email,password=pwd)
				user.save()
				# Create new user in mmclient also
				
				
			except:
				print "USERNAME NOT UNIQUE" 
				# Add error message here 
				return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))

			return HttpResponseRedirect('/thanks/')
	else:
        	form = forms.SignUp() # An unbound form

	return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))

def thanks(request):
	'''
	View for User Profile
	'''
	return render_to_response('welcome.html',context_instance=RequestContext(request))

@login_required
def profile(request):
	'''
	View for User Profile
	'''
	
	#Getting Gravatar Image
	email = request.user.email
	size=150
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'s':str(size)})
	
	# If login form is already submitted
	if request.method == 'POST':# or request.method =='GET': 
		#The constructor has been overridden. [] necessary
		form = forms.Profile([],request.POST) 
		if form.is_valid(): 
			# Process the data in form.cleaned_data
			print "CLEANED DATA", form.cleaned_data
			print form.cleaned_data['id_display_name0']
	else:
		profile_details = mmclient.getProfileDetails(email)
        	form = forms.Profile(profile_details) # Create new form
	
	return render_to_response('profile.html', {'gurl': gravatar_url, 'form':form}, context_instance=RequestContext(request))
	
	

@login_required
def preferences(request):
	'''
	Show and edit user preferences
	'''
	prefs = mmclient.getUserPreferences(request.user.email)
	return render_to_response('preferences.html', {'prefs': prefs}, context_instance=RequestContext(request))

@login_required
def logout(request):
	'''
	View for user logout
	'''
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")

@login_required
def subscribe(request, fqdn_listname):
	''' 
	Subscribe to list with fqdn_listname = fqdn_listname
	'''
	success = mmclient.subscribe(request.user.email, fqdn_listname)
	return HttpResponseRedirect("/lists")

@login_required
def unsubscribe(request, fqdn_listname):
	''' 
	Subscribe to list with fqdn_listname=fqdn_listname
	'''
	success = mmclient.unsubscribe(request.user.email, fqdn_listname)
	return HttpResponseRedirect("/lists")

