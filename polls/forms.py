from django import forms
from django.forms import DateInput, inlineformset_factory
from .models import Poll, Options
from crispy_forms.helper import FormHelper #controls what is displayed by crispy forms
from django.utils import timezone
from djangoformsetjs.utils import formset_media_js

class PollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None) #automatic form layout
        self.helper = FormHelper()

    # def clean(self):
    #     print(self)
    #     return self

    class Meta:
        model = Poll
        fields = ["form", "pub_date"]
        widgets = {
            "pub_date": forms.SelectDateWidget(),
            "form": forms.TextInput
         }
        labels = {
            "form": "Poll Name"
        }
        initial = {
            "pub_date": timezone.now()
        }

    class Media(object):
        js = formset_media_js

class OptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Options
        fields = ["option"]

OptionFormSet = inlineformset_factory(Poll, Options, OptionForm, extra=1)

