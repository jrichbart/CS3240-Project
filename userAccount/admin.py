from django.contrib import admin

# Register your models here.

from .models import userAccount, Course, Availability, buddies, ZoomMeeting

admin.site.register(userAccount)

admin.site.register(Course)

admin.site.register(Availability)

admin.site.register(buddies)

admin.site.register(ZoomMeeting)
