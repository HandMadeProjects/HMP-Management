from django.contrib import admin

# Register your models here.

from .models import UserData, RequestData, ProjectData

# # Register your models here.

admin.site.register(UserData)
admin.site.register(RequestData)
admin.site.register(ProjectData)