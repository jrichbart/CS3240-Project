from django.db import models

# Create your models here.
class Account(models.Model):
    acc_name = models.CharField(max_length=50)
    acc_password = models.CharField(max_length=50)
    def __str__(self):
        return self.acc_name