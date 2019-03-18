from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import randomcolor
from django.shortcuts import reverse

#this is the parent class
class Poll(models.Model):#define fields and behaviors
    form = models.CharField(max_length=255)
    pub_date = models.DateField(default=timezone.now)
    text = models.CharField(max_length=255, null='DEFAULT VALUE')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    #text is used as a keyword, which is useful for categorising

    def __str__(self):
        return str(self.text) #convert to string to avoid any errors

    def get_absolute_url(self):
        return reverse('polls:poll_results', kwargs={'poll_id': self.id})

def generate_random_color():
    rand_color = randomcolor.RandomColor()
    color = rand_color.generate(format_="hex", luminosity="bright")[0].lstrip("#")
    rgba_color = "rgba" + str(tuple(int(color[i:i+2], 16) for i in (0, 2 ,4)) + (1.0, ))
    return rgba_color


#this is the child class
class Options(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE) #many to one relationship, relating to the Poll class
    option = models.CharField(max_length=255) #choice_text
    votes = models.IntegerField(default=0) #0 votes on the choice to start off with
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    option_color = models.CharField(max_length=32, default=generate_random_color)

    def __str__(self):
        return "{} - {}".format(self.question.form[:25], self.option[:25]) #slicing


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

#points to object, views the object
