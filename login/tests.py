from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from userAccount.models import userAccount, Course, buddies

def create_user(user, first_name, last_name, major, bio):
    """
    creates a userAccount with the given user and name arguments
    """
    return userAccount.objects.create(user=user, first_name=first_name, last_name=last_name, major=major, bio=bio)

# Create your tests here.
class LoginViewTests(TestCase):
    def test_view_login(self):
        """
        tests to if login page displays login with google
        """
        url = reverse('login:login')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "Sign In With Google")

    def test_view_home(self):
        """
        tests to see if user with an account is directed to the correct page
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        login = self.client.force_login(testUser)
        url = reverse('login:home')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "Are you ready")

    def test_view_home_2(self):
        """
        tests to see if user without an account is directed to the correct page
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        login = self.client.force_login(testUser)
        url = reverse('login:home')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "First")    