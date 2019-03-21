from django.contrib import admin
from .models import *
# Register your models here.
# the . simply means that the import is from the same directory


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Options)
admin.site.register(Poll)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments)
admin.site.register(UserProfile)
