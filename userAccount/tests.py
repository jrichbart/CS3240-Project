from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

from .models import userAccount

class userAccountModelTest(TestCase):
    def test_self_str(self):
        """
        userAccount returns name property
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testAccount = userAccount(user=testUser, name="John Doe")
        self.assertEqual(str(testAccount),"John Doe")

class userAccountHasAccountViewTests(TestCase):
    def test_logged_in(self):
        """
        logged in users get redirected to account page
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        login = self.client.force_login(testUser)
        url = reverse('userAccount:has_account')
        response = self.client.get(url)
        self.assertRedirects(response, '/profile/')

    def test_not_logged_in(self):
        """
        not logged in users get redirected to login page
        """
        url = reverse('userAccount:has_account')
        response = self.client.get(url)
        self.assertRedirects(response, '/')

def create_user(user, name):
    """
    creates a userAccount with the given user and name arguments
    """
    return userAccount.objects.create(user=user,name=name)

class userAccountViewAccountViewTests(TestCase):
    def test_view_account(self):
        """
        user's name shows up in response when account is already set up
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, name="John Doe")
        login = self.client.force_login(testUser)
        url = reverse('userAccount:has_account')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "John Doe")

class userAccountSaveViewTests(TestCase):
    def test_update_account(self):
        """
        name updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, name="John Doe")
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save')
        data = {'acc_name' : 'James'}
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:view_account'))
        self.assertContains(response, "James")