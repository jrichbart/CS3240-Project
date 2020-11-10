from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from userAccount.models import userAccount, Course, buddies

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

class findViewBuddyRequestTests(TestCase):

    def test_request_view(self):
        """
        desired buddy's name shows up in response when account is already set up
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        create_course(uA, "CS", "3240")
        login = self.client.force_login(testUser)
        url = reverse('find:view_send_request', kwargs={'user': "testUser"})
        response = self.client.get(url, follow=True)
        self.assertContains(response, "John")

    def test_send_request(self):
        """
        user can send a buddy request to someone
        """
        testUser1 = User.objects.create_user(username="testUser1", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser1, first_name="John", last_name="Doe", major='', bio='')
        testUser2 = User.objects.create_user(username="testUser2", email = "email@virginia.edu", password="testPassword")
        uB = create_user(user=testUser2, first_name="Jane", last_name="Doe", major='', bio='')
        create_course(uA, "CS", "3240")
        create_course(uB, "CS", "3240")
        login = self.client.force_login(testUser1)
        url = reverse('find:view_buddy_request', kwargs={'user': "testUser2"})
        data = {
            'request_message_input' : "this is a test"
        }
        self.client.post(url,data)
        self.assertEquals((buddies.objects.get(request_message="this is a test").requestee.user.username), "testUser2")
        