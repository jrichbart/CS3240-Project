from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from userAccount.models import userAccount

def create_user(user, name, major, bio):
    """
    creates a userAccount with the given user and name arguments
    """
    return userAccount.objects.create(user=user,name=name, major=major, bio=bio)

class findViewIndexViewTests(TestCase):

    def test_view_account(self):
        """
        user's name shows up in response when account is already set up
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, name="John Doe", major='', bio='')
        login = self.client.force_login(testUser)
        url = reverse('find:index')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "John Doe")