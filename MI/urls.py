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
	(r'^reply/(.+)$', views.reply),
	(r'^archives/$', views.archives),
	(r'^archives/(\d+)/$', views.archives),
	(r'^lists/$', views.lists),
	(r'^subscribe/(.+)/$', views.subscribe),
	(r'^unsubscribe/(.+)/$', views.unsubscribe),
	(r'^profile/$', views.profile),
	(r'^preferences/$',views.preferences),
	(r'^newuser/$', views.newuser),
	(r'^thanks/$', views.thanks),
	(r'^logout/$',views.logout),
	(r'^admin/', include(admin.site.urls)),
)

urlpatterns += django.contrib.staticfiles.urls.staticfiles_urlpatterns()
