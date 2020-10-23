from django.contrib import admin

# Register your models here.

from .models import userAccount, Course, Availability

admin.site.register(userAccount)

admin.site.register(Course)

admin.site.register(Availability)
