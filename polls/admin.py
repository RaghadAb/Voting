from django.contrib import admin
from .models import Poll, Options, Category, Comments, UserProfile
# Register your models here.
# the . simply means that the import is from the same directory


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Options)
admin.site.register(Poll)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments)
admin.site.register(UserProfile)
