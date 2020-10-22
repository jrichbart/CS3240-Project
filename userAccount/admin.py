from django.contrib import admin

# Register your models here.

from .models import userAccount, Course

admin.site.register(userAccount)

admin.site.register(Course)
