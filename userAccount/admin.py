from django.contrib import admin

# Register your models here.

from .models import userAccount, Course, Availability, buddies

admin.site.register(userAccount)

admin.site.register(Course)

admin.site.register(Availability)

admin.site.register(buddies)
