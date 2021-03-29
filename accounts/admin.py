from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


admin.site.site_header = 'Administration'


class UserProfileAdmin(admin.ModelAdmin):
    list_display =('user','mobile','address')
    list_filter = ('address',)

    def mobile(self,obj):
        return obj.mobile


admin.site.register(UserProfile, UserProfileAdmin)

