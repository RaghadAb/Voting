from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.forms.models import BaseInlineFormSet
from django.core.files.storage import FileSystemStorage


#note: formsets keep track of the initial form created, and the changes done to them afterwards.
#inline formsets are used to handle set of objects belong to common foreign key.
def index(request):
	return render(request,'index.html')

def header(request):
	return render(request,'header.html')

@login_required
def createpoll(request):
	if request.method == "POST":
		form = PollForm(request.POST)
		if form.is_valid():
			poll = form.save(commit=False) #this gives a model object which you can edit and then save. hence the poll.save()
			poll.author = request.user
			poll.save()
			messages.add_message(request, messages.INFO, 'Poll created!')
			return HttpResponseRedirect(reverse("polls:showpoll", kwargs={ "poll_id": poll.id }))   #arguments, redirect to a specific url, reverse is used incase non match is for the url is found
	form = PollForm()
	return render(request,'createpoll.html', { 'form': form })#combines the template with the dictionary

def show_poll(request, poll_id):
	option=Poll.objects.get(id=poll_id)
	comments = Comments.objects.filter(poll=poll_id)

	if request.method=="POST":
		print("It's submitted!")
		print(request.POST)

	context={'option':option, 'comments':comments}
	return render(request,'show_poll.html',context)

def myaccount(request):
	return render(request,'myaccount.html')

def mypolls(request):
	polls = Poll.objects.filter(author=request.user)
	context = { "polls": polls }
	return render(request,'mypolls.html', context)


def search(request):
	empty_query = False
	search_query = request.GET.get("q") #q is any input which is passed in the search field, incase a query is passed it will be picked up, otherwise it is left alone
	_filter = request.GET.get("filter")
	if search_query == None or len(search_query.strip()) == 0:
		empty_query = True
		polls = []
	else:
		polls = Poll.objects.filter(form__icontains=search_query) #filtering the word which has been used to search for a poll
		if not _filter or _filter == "recent":
			polls = polls.order_by('-created_at')
		elif _filter == "popular":
			polls = polls.order_by("-votes")
	context={
		'polls':polls,
		'empty_query': empty_query
	}
	return render(request,'search.html',context)

def vote(request, quickPoll_id):
        comments = Comments.objects.filter(poll=quickPoll_id)
        if request.method=='POST':
                selected_option = Options.objects.filter(id=request.POST['choice'])[0]
                selected_option.votes+=1
                selected_option.save()
                poll=selected_option.question
                poll.votes+=1
                poll.save()
        context = { 'poll': poll, 'comments':comments}
        return render(request,'results.html', context)

def poll_results(request, poll_id):
        poll = get_object_or_404(Poll,id=poll_id)
        context={'poll':poll}
        return render(request,'search.html',context)

def all_urls(request):
	return render(request,'all_urls.html')


def my_voted_polls(request):
	polls = Poll.objects.filter(author=request.user, vote__voter__pk=request.user.id)
	context = { "polls": polls }
	return render(request,'mypolls.html', context)

class OptionInline(InlineFormSetFactory): #create multiple model instances from a single form, option in this case
    model = Options #for multiple options in a single form
    fields = ['option']


class PollFormClass(BaseInlineFormSet): #nested formset
	def clean(self): #this is done to perform validation checks
		print(self)
		return


class TestView(CreateWithInlinesView):
	model = Poll
	form_class = PollForm
	inlines = [OptionInline]
	template_name = "polls/poll_form.html"

	def forms_valid(self, form, inlines):
		form.instance.author = self.request.user
		return super(TestView, self).forms_valid(form, inlines)

	def get_formset_kwargs(self):
		kwargs = super(TestView, self).get_formset_kwargs()
		# modify kwargs here, modification at run time
		print(kwargs)
		return kwargs

	def get_factory_kwargs(self):
		kwargs = super(TestView, self).get_factory_kwargs()
		# modify kwargs here
		print(kwargs)
		print("^factry")
		return kwargs

	def get_success_url(self):
		return reverse('polls:showpoll', kwargs={'poll_id': self.object.id}) #check to see if any kwargs have been passed to it

def add_comment(request, quickPoll_id):
        poll = get_object_or_404(Poll, id=quickPoll_id)
        if request.method=='POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.poll=poll
                        comment.author=request.user
                        comment.save()
                        return redirect('polls:index')
                else:
                        form = CommentForm()
                context={'form':form}
                return render(request,"add_comment.html", context)

def register(request):
        registered = False
        if request.method == 'POST':
                user_form = UserForm(data=request.POST)
                profile_form = UserProfileForm(data=request.POST)
                if user_form.is_valid() and profile_form.is_valid():
                        user = user_form.save()
                        user.set_password(user.password)
                        user.save()
                        profile = profile_form.save(commit=False)
                        profile.user=user
                        if 'picture' in request.FILES:
                                profile.picture = request.FILES['picture']
                        profile.save()
                        registered = True
                else:
                        print(user_form.errors, profile_form.errors)
        else:
                user_form=UserForm()
                profile_form=UserProfileForm()
        return render(request,
                      'register.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'registered':registered})
