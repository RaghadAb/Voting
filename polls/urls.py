from django.conf.urls import url
from django.urls import path, include
from polls import *
from django.conf import settings
from django.conf.urls.static import static


app_name='polls'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'header.html', views.header, name='header'),
	url(r'^createpoll', views.createpoll, name='createpoll_legacy'),
	url(r'^showpoll/(?P<poll_id>\d+)/', views.show_poll, name='showpoll'),
	url(r'^myaccount', views.myaccount, name='myaccount'),
	url(r'^mypolls', views.mypolls, name='mypolls'),
	url(r'^search', views.search, name='search'),
	url(r'^option/(?P<quickPoll_id>\d+)/', views.show_poll,name='showpoll'),
        url(r'^polls/(?P<quickPoll_id>\d+)/vote/', views.vote, name='vote'),
	url(r'^test', views.TestView.as_view(), name='createpoll'),
        url(r'^add_comment/(?P<quickPoll_id>\d+)', views.add_comment, name='add_comment'),
        url(r'^register/$', views.register, name='register'),
        url(r'^results/(?P<quickPoll_id>\d+)/', views.show_results, name='show_results'),
	path('profile_images/', views.UserProfile, name='UserProfile'),
	path('accounts/', include('django.contrib.auth.urls')),


]
