from django.contrib import admin
from .models import Poll, Options
# Register your models here.
# the . simply means that the import is from the same directory


admin.site.register(Options)
admin.site.register(Poll)