from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class userAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    major = models.CharField(max_length=50)
    bio = models.TextField()
    computing_id = models.CharField(max_length=7)
    phone_number = models.CharField(max_length=15)
    discord_name = models.CharField(max_length=50)
    def __str__(self):
        return self.first_name + " " + self.last_name

    def getCourses(self):
        return self.courses.all()

    def getBuddies(self):
        requested = self.requester.all()
        requestee = self.requestee.all()
        accepted = []
        pendingYourApproval = []
        pendingTheirApproval = []
        for buddy in requested:
            if buddy.approved:
                accepted.append(buddy.requestee)
            else:
                pendingTheirApproval.append(buddy.requestee)
        for buddy in requestee:
            if buddy.approved:
                accepted.append(buddy.requester)
            else:
                pendingYourApproval.append(buddy.requester)
        return {"accepted" : accepted, "pendingYourApproval" : pendingYourApproval, "pendingTheirApproval" : pendingTheirApproval}
        
    def getSharedCourses(self, user2):
        self_courses = self.courses.all()
        user2_courses = user2.courses.all()
        shared = [course for course in self_courses if course in user2_courses] 
        return shared

class Course(models.Model):
    student = models.ForeignKey(userAccount, related_name='courses', on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=4)
    number = models.CharField(max_length=4)
    def __str__(self):
        return self.mnemonic + self.number + " for " + str(self.student)
    def __eq__(self, other):
        if isinstance(other, Course):
            return (self.number == other.number and self.mnemonic == other.mnemonic)
        return False
    def __hash__(self):
        return super().__hash__()

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
