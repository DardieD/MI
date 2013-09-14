import django.contrib.staticfiles.urls 
from django.conf.urls import patterns, include, url
from MI import views, settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
	(r'^$', views.welcome),
	(r'^home/$', views.home ),
	(r'^conversation/(.+)$', views.conversation ), 
	(r'^compose/$', views.compose),
	
	(r'^reply/(?P<subject>.+)/(?P<msgid>.+)/(?P<rec>.+)/(?P<message>.+)$', views.reply),
	
	(r'^archives/$', views.archives),
	
	
	(r'^lists/$', views.lists),
	(r'^subscribe/(.+)/$', views.subscribe),
	(r'^unsubscribe/(.+)/$', views.unsubscribe),
	
	(r'^publicprofile/(.+)/$', views.publicprofile),
	(r'^profile/$', views.profile),
	(r'^useraway/$', views.useraway),
	(r'^changepwd/$', views.changepwd),
	
	(r'^preferences/$',views.preferences),
	(r'^newuser/$', views.newuser),
	(r'^thanks/$', views.thanks),
	(r'^logout/$',views.logout),
	(r'^admin/', include(admin.site.urls)),
)

urlpatterns += django.contrib.staticfiles.urls.staticfiles_urlpatterns()
