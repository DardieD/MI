import django.contrib.staticfiles.urls 
from django.conf.urls import patterns, include, url
from MemberInterface import views, settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
	(r'^$', views.welcome),
	(r'^home/(.+)/$', views.home ),
	(r'^compose/$', views.compose),
	(r'^archives/$', views.archives),
	(r'^archives/(\d+)/$', views.archives),
	(r'^lists/$', views.lists),
	(r'^profile/$', views.profile),
	(r'^newuser/$', views.newuser),
)

urlpatterns += django.contrib.staticfiles.urls.staticfiles_urlpatterns()