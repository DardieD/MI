from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import forms
from use_client import t
from Message import Message
from django.contrib.auth.models import User
from django.contrib import auth

def test(reuest):
	'''
	Testing mailman.client in app
	'''
	return render_to_response('testhtml.html', {'fromclient':t()})

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
    		# Authenticated user
		#create message object
		amessage = Message()
		#create message dictionary for template
		#mslist = amessage.getMessage() #throws error: getMessage() takes no arguments one given
		#dummy data
		mslist = {'subject':amessage.subject, 'author':amessage.author,'date':amessage.date, 'listname':amessage.listname, 'msg':amessage.msg,'msgid':amessage.msgid}
		#return render_to_response('home.html', {'Username':user,'mslist':mslist})
		return render_to_response('home.html', {'mslist':mslist}, context_instance=RequestContext(request))

	else:
		# Anonymous user
		mslist = {'subject':"Anonymous", 'author':"Anonymous",'date':"No Date", 'listname':"No list", 'msg':"Sorry, you need to login" ,'msgid':"00927"}
		#return render_to_response('home.html', {'Username':"Anonymous User",'mslist':mslist})
		return render_to_response('home.html', {'mslist':mslist}, context_instance=RequestContext(request))
	
def compose(request):
	'''
	View for the compose screen
	Add parameters to take subject and recepients list
	in case of 'reply'
	'''
	#To be added: compose/new and compose/reply

	# If form is already submitted
	if request.method == 'POST' or request.method =='GET': 
		form = forms.Compose(request.POST)
		if form.is_valid(): 
			# Process the data in form.cleaned_data
			return HttpResponseRedirect('/compose/')
	else:
        	form = forms.Login() # An unbound form

	return render_to_response('compose.html', {'form': form}, context_instance=RequestContext(request))


def archives(request):
	'''
	View for the archives
	'''
	return render_to_response('archives.html')

def lists(request):
	'''
	View for rendering all available lists
	? Need user_id to access user's subscribed lists 
	'''
	return render_to_response('lists.html')

def profile(request):
	'''
	View for User Profile
	'''
	return render_to_response('profile.html')

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
			print name, pwd, email, essay
			user = User.objects.create_user(username=name,email=email,password=pwd)
			user.save()
			return HttpResponseRedirect('/thanks/')
	else:
        	form = forms.SignUp() # An unbound form

	return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):
	'''
	View for user logout
	'''
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")

