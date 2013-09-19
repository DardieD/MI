from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib import messages

from mailclient import mmclient
from MI import models
from MI.view import MessageRenderer, FavoriteRenderer
import forms

from sqlite3 import IntegrityError

import urllib, hashlib

def welcome(request):
	'''
	View for welcome screen
	Welcome is a public screen that shows static information 
	that may be displayed as well as the login and signup forms. 
	'''
	#If user is already logged in, redirect to homescreen
	if request.user.is_authenticated():
		return HttpResponseRedirect("/home")
	
	# LOGIN Form
	# If login form is already submitted
	if request.method == 'POST': 
		form = forms.Login(request.POST)
		if form.is_valid(): 
			# Process the data in form.cleaned_data
			#responseurl = '/home/' + form.cleaned_data['username'] + '/' ; 
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = auth.authenticate(username=username, password=password)
			if user is not None: #and user.is_active:
				# Correct password, and the user is marked "active"
				auth.login(request, user)
				# Redirect to a success page.
				return HttpResponseRedirect("/home/")
			else:
				# Show an error page
				messages.error(request, "Invalid Login Credentials")
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
		mslist = MessageRenderer.getLatestMessages(request.user.email)
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
		mslist = MessageRenderer.getMessageByThreadID(threadid)
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
			mssg_sent = send_mail(subject,message,sender,recipient, fail_silently=False)
			if mssg_sent == 1:
				messages.info(request, "Message sent successfully.")
			else:
				messages.error(request, "Something happened and we couldn't send that email.")
			return HttpResponseRedirect('/home/')
	else:
        	form = forms.Compose(request.user.email) # An unbound form
	
	return render_to_response('compose.html', {'form': form}, context_instance=RequestContext(request))
	
	
@login_required
def reply(request, subject, msgid, rec, message):
	'''
	View for the Reply screen
	Replying to message with subject and msgid given 
	Recipient is the rec list
	'''
	
	sender = request.user.email
	
	recipient = []
	recipient.append(rec)
	
	# If Re: not in the subject line, append "Re:"	
	if "Re:" not in subject and '[' in subject:
		splits = subject.split(']',1);
		subject = splits[0] + "] Re: " + splits[1]
	else:
		subject = "Re: " + subject
	
	mssg = EmailMessage(subject,message,sender,recipient,  headers = {'In-Reply-To': msgid})
	mssg_sent = mssg.send()
	if mssg_sent == 1:
		messages.info(request, "Reply sent successfully.")
	else:
		messages.error(request, "Something happened and we couldn't send that email.")
	
	return HttpResponseRedirect('/home/')
	
def archives(request):
	'''
	View for the archives
	'''
	if request.method == 'POST': 
		form = forms.ArchiveRenderer(request.user.email, request.POST)
		if form.is_valid(): 
			listname = form.cleaned_data['listnames']
			to_date = form.cleaned_data['to_date']
			from_date = form.cleaned_data['from_date']
			mslist = MessageRenderer.getMessagesBasicAchive(listname, from_date, to_date)
			if not mslist:
				#MSLIST is empty
				messages.error(request, "No messages for "+ listname +  " list from " + str(from_date) + " to " + str(to_date))
			return render_to_response('archives.html', {'mslist':mslist}, context_instance=RequestContext(request))
	else:
        	form = forms.ArchiveRenderer(request.user.email) # An unbound form
	
	return render_to_response('archives.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def favorites(request):
	'''
	Accessing favorites list
	'''
	mslist = FavoriteRenderer.getFavorites(request.user.email)
	return render_to_response('favorites.html', {'mslist': mslist}, context_instance=RequestContext(request))

@login_required
def addfavorites(request, msgid):
	'''
	Adding to and accessing favorites list
	'''
	msg = FavoriteRenderer.addToFavorites(request.user.email, msgid)
	messages.info(request, msg)
	mslist = FavoriteRenderer.getFavorites(request.user.email)
	return HttpResponseRedirect('/home')

	
@login_required
def removefavorites(request, msgid):
	'''
	Removing from favorites list
	'''
	msg = FavoriteRenderer.removeFromFavorites(request.user.email, msgid)
	messages.info(request, msg)
	mslist = FavoriteRenderer.getFavorites(request.user.email)
	#return HttpResponseRedirect('/home')
	return render_to_response('favorites.html', {'mslist': mslist}, context_instance=RequestContext(request))
	
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
				# Create new user in mmclient
				mmclient.createUser(username=name, email=email, password=pwd)
				
				#Create user in system
				user = User.objects.create_user(username=name,email=email,password=pwd)
				user.save()
				
			except Exception as ex:
				messages.error(request, "THE USERNAME/EMAIL ID IS ALREADY IN THE SYSTEM")
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
	messages.info(request, "THANK YOU FOR SIGNING UP !")
	return HttpResponseRedirect("/")


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
	
	#Getting User Status for App
	status = "Active" if request.user.is_active==True else "Gone Fishin'"

	# If form is already submitted
	if request.method == 'POST':
		#The constructor has been overridden. [] necessary
		form = forms.Profile(request.POST) 
		if form.is_valid(): 
			# set Profile Details
			old_name = mmclient.getUserName(email)
			msg = mmclient.setProfileDetails(email, form.cleaned_data)
			messages.info(request, msg)
			#Change all occurances of old_name to new_name in the db
			msg = MessageRenderer.updateScreenname(old_name,form.cleaned_data['display_name'])

		return HttpResponseRedirect("/profile")
	else:
		#Get dictionary from mmclient
		profile_details = mmclient.getProfileDetails(email)
        	form = forms.Profile(profile_details) # Create new form
        	pwdform = forms.ChangePwd()
		return render_to_response('profile.html', {'gurl': gravatar_url, 'form':form, 'pwdform':pwdform, 'status':status}, context_instance=RequestContext(request))
	
@login_required
def publicprofile(request, profile_email):
	'''
	Render public profile of user 
	with email id = profile_email
	'''
	
	#Getting Gravatar Image
	email = profile_email
	size=150
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'s':str(size)})
	
	#Getting User Status for App
	u = User.objects.get(email__exact=email)
	status = "Active" if u.is_active==True else "Gone Fishin'"
	
	#Getting User's Display Name
	display_name = mmclient.getUserName(email)
	
	return render_to_response('publicprofile.html', {'gurl': gravatar_url, 'status':status, 'display_name':display_name}, context_instance=RequestContext(request))
	
def changepwd(request):
	'''
	Change user's password
	'''
	email=request.user.email
	# If form is already submitted
	if request.method == 'POST':
		#The constructor has been overridden. [] necessary
		pwdform = forms.ChangePwd(request.POST) 
		if pwdform.is_valid(): 
			#Authenticate based on old password			
			user = auth.authenticate(username=request.user.username, password=pwdform.cleaned_data['old_pwd'])
			if user is not None: 
				# Correct password
				pwd = pwdform.cleaned_data['new_pwd']
				msg = mmclient.changePwd(email,pwd)
				messages.info(request, msg)
				return HttpResponseRedirect("/profile")

			else:
				#Old password Authentication Failes
				messages.error(request, "Incorrect Old Password: Cancelling Password Change Request")
				return HttpResponseRedirect("/profile")
	
	return HttpResponseRedirect("/profile")
        	
	#return render_to_response('home.html',context_instance=RequestContext(request))
	
def useraway(request):
	'''
	Mark user as 'away'
	Django docs recommend marking user as inactive
	rather than deleting user since deleting a user
	causes foreign keys to break
	'''
	request.user.is_active = False if request.user.is_active==True else True
	request.user.save()
	return HttpResponseRedirect("/profile")

@login_required
def preferences(request):
	'''
	Show and edit user preferences
	'''
	# If form is already submitted
	if request.method == 'POST':
		#The constructor has been overridden. [] necessary
		form = forms.Preferences(request.POST) 
		if form.is_valid(): 
			msg = mmclient.setUserPreferences(request.user.email, form.cleaned_data)
			messages.info(request, msg)
		else:
			messages.info(request, "An error occured. Please try again")
			return HttpResponseRedirect("/preferences")
	else:
		#Get dictionary from mmclient
		initial_prefs = mmclient.getUserPreferences(request.user.email)
        	form = forms.Preferences(initial=initial_prefs) # Create new form

	prefs = mmclient.getUserPreferences(request.user.email)
	return render_to_response('preferences.html', {'prefs': prefs, 'form':form}, context_instance=RequestContext(request))


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


