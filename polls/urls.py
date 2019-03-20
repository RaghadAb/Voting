from django.conf.urls import url
from polls import views

app_name="polls"

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'header.html', views.header, name='header'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),
	url(r'^createpoll', views.createpoll, name='createpoll_legacy'),
	url(r'^showpoll/(?P<poll_id>\d+)/', views.show_poll, name="showpoll"),
	url(r'^results/(?P<poll_id>\d+)/', views.poll_results, name="poll_results"),
	url(r'^myaccount', views.myaccount, name='myaccount'),
	url(r'^mypolls', views.mypolls, name='mypolls'),
	url(r'^search', views.search, name='search'),
	# url(r'^vote', views.vote, name='vote'),
	# url(r'^results', views.results, name='results'),
	url(r'^all_urls', views.all_urls, name='all_urls'),
	url(r'^option/(?P<quickPoll_id>\d+)/', views.show_poll,name='showpoll'),
    url(r'^polls/(?P<quickPoll_id>\d+)/vote/', views.vote, name='vote'),
	url(r'^test', views.TestView.as_view(), name='createpoll'),
	url("voted/", views.my_voted_polls, name="my_voted_polls"),
]
