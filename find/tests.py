from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from userAccount.models import userAccount, Course

def create_user(user, first_name, last_name, major, bio):
    """
    creates a userAccount with the given user and name arguments
    """
    return userAccount.objects.create(user=user, first_name=first_name, last_name=last_name, major=major, bio=bio)

def create_course(student, mnemonic, number):
    """
    creates a userAccount with the given user and name arguments
    """
    return Course.objects.create(student=student,mnemonic=mnemonic, number=number)

class findViewIndexViewTests(TestCase):

    def test_view_account(self):
        """
        user's name shows up in response when account is already set up
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        create_course(uA, "CS", "3240")
        login = self.client.force_login(testUser)
        url = reverse('find:index')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "CS 3240")