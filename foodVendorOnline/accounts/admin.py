from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('email','username','first_name','last_name','role','is_active')
    filter_horizontal =()
    list_filter = ()
    fieldsets = ()
    ordering=('-date_joined',)



admin.site.register(User,UserAdmin)
admin.site.register(UserProfile)