from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from .models import Poll, Options, Vote
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
			return HttpResponseRedirect(reverse("polls:showpoll", kwargs={ "poll_id": poll.id }))
	form = PollForm()
	return render(request,'createpoll.html', { 'form': form })

def show_poll(request, poll_id):
	poll = get_object_or_404(Poll, id=poll_id)
	return render(request,'show_poll.html', { 'poll': poll })

def myaccount(request):
	return render(request,'myaccount.html')

def mypolls(request):
	return render(request,'mypolls.html')

def search(request):
	polls= Poll.objects.all()
	context={'polls':polls}
	return render(request,'search.html',context)

def vote(request, quiPoll_id):
	poll = get_object_or_404(Poll, id=quiPoll_id)
	try:
		print(request.POST["option"])
		selected_option = poll.options_set.get(pk=request.POST["option"])
		with transaction.atomic():
			selected_option.votes += 1
			poll.votes += 1
			vote = Vote()
			if request.user.is_authenticated:
				vote.voter = request.user
			vote.option = selected_option
			vote.poll = poll
			vote.save(); selected_option.save(); poll.save();

	except (KeyError, Options.DoesNotExist) as e:
		print(e)
		pass
	return render(request,'vote.html')

def poll_results(request, poll_id):
	poll = get_object_or_404(Poll, id=poll_id)
	context = { 'poll': poll }
	return render(request,'results.html', context)

def all_urls(request):
	return render(request,'all_urls.html')

def option_Number(request, quiPoll_id):
    option=Poll.objects.get(id=quiPoll_id)

    if request.method=="POST":
        print("It's submitted!")
        print(request.POST)

    if request.method=="GET":
        print("Got it")
        print(request.GET)

    context={'option':option}
    return render(request,'option_Number.html',context)


class OptionInline(InlineFormSetFactory): #create multiple model instances from a single form, option in this case
    model = Options #for multiple options in a single form
    fields = ['option']


class PollFormClass(BaseInlineFormSet): #nested formset
	def clean(self):
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
		return reverse('polls:showpoll', kwargs={'poll_id': self.object.id})

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
