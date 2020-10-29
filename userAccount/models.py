from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class userAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    bio = models.TextField()
    def __str__(self):
        return self.name

class Course(models.Model):
    student = models.ForeignKey(userAccount, related_name='courses', on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=4)
    number = models.CharField(max_length=4)
    def __str__(self):
        return self.mnemonic + self.number + " for " + str(self.student)

class Availability(models.Model):
    student = models.ForeignKey(userAccount, related_name='availability', on_delete=models.CASCADE, unique=True)
    calendar = models.CharField(max_length=112)

class buddies(models.Model):
    requester = models.ForeignKey(userAccount, related_name='requester', on_delete=models.CASCADE)
    requestee = models.ForeignKey(userAccount, related_name='requestee', on_delete=models.CASCADE)
    request_message = models.TextField()
    approved = models.BooleanField()
    denied_message = models.TextField()
    denied = models.BooleanField()