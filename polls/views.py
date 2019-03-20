from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from .models import Poll, Options, Vote,Category, Comments
from .forms import PollForm, OptionFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.forms.models import BaseInlineFormSet

#note: formsets keep track of the initial form created, and the changes done to them afterwards.
#inline formsets are used to handle set of objects belong to common foreign key.
def index(request):
	return render(request,'index.html')

def header(request):
	return render(request,'header.html')

def login(request):
	return render(request,'login.html')

def register(request):
	return render(request,'register.html')

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
	poll = get_object_or_404(Poll, id=quickPoll_id)
	try:
		print(request.POST["option"])
		selected_option = poll.options_set.get(pk=request.POST["option"])
		with transaction.atomic(): #if there is an error, it redirects it automatically
			selected_option.votes += 1
			poll.votes += 1
			vote = Vote()
			if request.user.is_authenticated:
				vote.voter = request.user
			vote.option = selected_option
			vote.poll = poll
			vote.save(); selected_option.save(); poll.save();

	except (KeyError, Options.DoesNotExist) as e:#when you try to access a key which doesnt exist
		print(e)
		pass
	return render(request,'vote.html')

def poll_results(request, poll_id):
	poll = get_object_or_404(Poll, id=poll_id)
	context = { 'poll': poll }
	return render(request,'results.html', context)

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



# class TestView(CreateView):
# 	model = Poll
# 	form_class = PollForm

# 	def get_context_data(self, **kwargs):
# 		data = super(TestView, self).get_context_data(**kwargs)
# 		if self.request.POST:
# 			data["poll_options"] = OptionFormSet(self.request.POST)
# 		else:
# 			data["poll_options"] = OptionFormSet()
# 		return data

# 	def form_valid(self, form):
# 		context = self.get_context_data()
# 		poll_options = context["poll_options"]
# 		with transaction.atomic():
# 			self.object = form.save()

# 			if poll_options.is_valid():
# 				poll_options.instance = self.object
# 				poll_options.save()
# 		return super(TestView, self).form_valid(form)
