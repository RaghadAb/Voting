from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural='categories'

    def __str__(self):
        return str(self.name)

#this is the parent class
class Poll(models.Model):#define fields and behaviors
    form = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#at this point, this is for registered users
    votes = models.IntegerField(default=0)
    #text is used as a keyword, which is useful for categorising

    def __str__(self):
        return str(self.form) #convert to string to avoid any errors

    def get_absolute_url(self):
        return reverse('polls:poll_results', kwargs={'poll_id': self.id})

#this is the child class
class Options(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE) #many to one relationship, relating to the Poll class
    option = models.CharField(max_length=255) #choice_text
    votes = models.IntegerField(default=0) #0 votes on the choice to start off with
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural='options'

    def __str__(self):
        return "{} - {}".format(self.question.form[:25], self.option[:25]) #slicing


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

#points to object, views the object

class Comments(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=2048, null=False)
    id = models.IntegerField(primary_key=True)
    poll = models.ForeignKey(Poll, null=False,on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='comments'

    def __str__(self):
        return str(self.text)


class UserProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return str(self.user.username)
