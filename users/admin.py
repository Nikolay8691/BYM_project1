from django.contrib import admin

from .models import Profile_user, Profile_admin

# Register your models here.
admin.site.register(Profile_admin)
admin.site.register(Profile_user)