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
    def __str__(self):
        return self.name

class course(models.Model):
    student = models.ForeignKey(userAccount, on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=4)
    number = models.CharField(max_length=4)