from django import forms
from django.forms import DateInput, inlineformset_factory
from .models import *
from crispy_forms.helper import FormHelper #controls what is displayed by crispy forms
from django.utils import timezone
from djangoformsetjs.utils import formset_media_js

class PollForm(forms.ModelForm): #a form is a single poll
    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None) #automatic form layout
        self.helper = FormHelper()

    # def clean(self):
    #     print(self)
    #     return self

    class Meta:
        model = Poll
        fields = ["form"]
        widgets = {
            "form": forms.TextInput
         } #these are the two fields displayed within a single form
        labels = {
            "form": "Poll Name"
        }

    class Media(object):
        js = formset_media_js

class OptionForm(forms.ModelForm): #this displays the options
    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper() #for multiple options

    class Meta:
        model = Options
        fields = ["option"]

OptionFormSet = inlineformset_factory(Poll, Options, OptionForm, extra=1) #create new objects and edit objects specified

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)   
        self.fields['text'].label = "Please enter your comments:"
    class Meta:
        model= Comments
        fields=('text',)
