from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

from .models import userAccount, Course, buddies

def create_user(user, name, major, bio):
    """
    creates a userAccount with the given user and name arguments
    """
    return userAccount.objects.create(user=user,name=name, major=major, bio=bio)


def create_course(student, mnemonic, number):
    """
    creates a userAccount with the given user and name arguments
    """
    return Course.objects.create(student=student,mnemonic=mnemonic, number=number)

def create_buddy(requester, requestee, approved):
    """
    creates a buddy relation with the given requester and requestee and approved value
    """
    return buddies.objects.create(requester=requester, requestee=requestee, request_message="", approved=approved, denied_message="", denied=False)

class userAccountModelTest(TestCase):
    def test_self_str(self):
        """
        userAccount returns name
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testAccount = userAccount(user=testUser, first_name="John", last_name="Doe")
        self.assertEqual(str(testAccount),"John Doe")
    def test_getCourses(self):
        """
        userAccount getCourses return list of associated courses
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testAccount = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        create_course(testAccount, "CS", "3240")
        create_course(testAccount, "MATH", "1010")
        self.assertEqual(list(testAccount.getCourses()), list(Course.objects.all()))
        
    def test_getBuddies_accepted(self):
        """
        userAccount get buddies returns the accepted buddies
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testRequestee = User.objects.create_user(username="testRequestee", password="testPassword")
        testAccount = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        testRequesteeAccount = create_user(user=testRequestee, first_name="John", last_name="Doe", major="CS", bio="sample")
        create_buddy(testAccount,testRequesteeAccount, True)
        self.assertEqual(testAccount.getBuddies()["accepted"][0],testRequesteeAccount)
    
    def test_getBuddies_their_approval(self):
        """
        userAccount get buddies returns the waiting for their approval buddies
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testRequestee = User.objects.create_user(username="testRequestee", password="testPassword")
        testAccount = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        testRequesteeAccount = create_user(user=testRequestee, first_name="John", last_name="Doe", major="CS", bio="sample")
        create_buddy(testAccount,testRequesteeAccount, False)
        self.assertEqual(testAccount.getBuddies()["pendingTheirApproval"][0],testRequesteeAccount)

    def test_getBuddies_your_approval(self):
        """
        userAccount get buddies returns the waiting for your approval buddies
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testRequester = User.objects.create_user(username="testRequester", password="testPassword")
        testAccount = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        testRequesterAccount = create_user(user=testRequester, first_name="John", last_name="Doe", major="CS", bio="sample")
        create_buddy(testRequesterAccount,testAccount, False)
        self.assertEqual(testAccount.getBuddies()["pendingYourApproval"][0],testRequesterAccount)
    
    def test_getSharedCourses(self):
        """
        userAccount get sharedCourses returns list of shared courses
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testUser2 = User.objects.create_user(username="testUser2", password="testPassword")
        testAccount = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        testAccount2 = create_user(user=testUser2, first_name="John", last_name="Doe", major="CS", bio="sample")
        shared = create_course(testAccount, "CS", "3240")
        create_course(testAccount, "MATH", "1010")
        create_course(testAccount2, "CS", "3240")
        create_course(testAccount2, "STS", "4500")
        self.assertEqual(testAccount.getSharedCourses(testAccount2),[shared])


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

def create_user(user, first_name, last_name, major, bio):
    """
    creates a userAccount with the given user and name arguments
    """
    return userAccount.objects.create(user=user,first_name=first_name, last_name=last_name, major=major, bio=bio)


def create_course(student, mnemonic, number):
    """
    creates a userAccount with the given user and name arguments
    """
    return Course.objects.create(student=student,mnemonic=mnemonic, number=number)

class userAccountViewAccountViewTests(TestCase):
    def test_view_account(self):
        """
        user's name shows up in response when account is already set up
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        login = self.client.force_login(testUser)
        url = reverse('userAccount:has_account')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "John")
        self.assertContains(response, "Doe")

class userAccountSaveViewTests(TestCase):
    def test_name_update_account(self):
        """
        name updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save')
        data = {
            'acc_first_name' : 'James',
            'acc_last_name' : 'Doe',
            'acc_major' : 'Psychology',
            'acc_bio' : '',
        }
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:view_account'))
        self.assertContains(response, "James")

    def test_major_update_account(self):
        """
        major updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save')
        data = {
            'acc_first_name' : 'John',
            'acc_last_name' : 'Doe',
            'acc_major' : 'Psychology',
            'acc_bio' : '',
        }
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:view_account'))
        self.assertContains(response, "Psychology")

    def test_bio_update_account(self):
        """
        bio updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save')
        data = {
            'acc_first_name' : 'John',
            'acc_last_name' : 'Doe',
            'acc_major' : 'Psychology',
            'acc_bio' : 'Hello I am John Doe',
        }
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:view_account'))
        self.assertContains(response, "Hello I am John Doe")

class CourseModelTests(TestCase):
    def test_self_str(self):
        """
        Course returns mnemonicnumber for name
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testAccount = userAccount(user=testUser, first_name="John", last_name="Doe")
        testCourse = Course(student=testAccount, mnemonic="CS", number = "3240")
        self.assertEqual(str(testCourse),"CS3240 for John Doe")
    def test_equals(self):
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testUser2 = User.objects.create_user(username="testUser2", password="testPassword")
        testAccount = create_user(user=testUser, first_name="James", last_name="", major="CS", bio="sample")
        testAccount2 = create_user(user=testUser2, first_name="John", last_name="", major="CS", bio="sample")
        course1 = create_course(testAccount, "CS", "3240")
        course2 = create_course(testAccount2, "CS", "3240")
        self.assertEqual(course1, course2)


class userAccountCourseViewTests(TestCase):
    def test_course_list(self):
        """
        account view should show list of courses associated with student acount
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        create_user(user=testUser, first_name="John", last_name="Doe", major='', bio='')
        login = self.client.force_login(testUser)
        testAccount = userAccount.objects.all()[0]
        create_course(student=testAccount, mnemonic="CS", number="3240")
        url = reverse('userAccount:view_account')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "CS 3240")

class userAccountContactSaveViewTests(TestCase):
    def test_computing_id_update(self):
        """
        computing id updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save_contact')
        data = {
            'computing_id' : 'abc1def',
            'phone_number' : '',
            'discord_name' : '',
        }
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:contact_info'))
        self.assertContains(response, "abc1def")
    def test_phone_number_update(self):
        """
        phone number updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save_contact')
        data = {
            'computing_id' : '',
            'phone_number' : '1111111111',
            'discord_name' : '',
        }
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:contact_info'))
        self.assertContains(response, "1111111111")
    def test_discord_name_update(self):
        """
        discord name updates when saved
        """
        testUser = User.objects.create_user(username="testUser", email = "email@virginia.edu", password="testPassword")
        uA = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        login = self.client.force_login(testUser)
        url = reverse('userAccount:save_contact')
        data = {
            'computing_id' : '',
            'phone_number' : '',
            'discord_name' : 'discordTest',
        }
        self.client.post(url,data)
        response = self.client.get(reverse('userAccount:contact_info'))
        self.assertContains(response, "discordTest")

class userAccountApproveBuddyViewTests(TestCase):
    def test_approve_buddy(self):
        """
        approving a buddy moves updates view
        """
        testUser = User.objects.create_user(username="testUser", password="testPassword")
        testRequester = User.objects.create_user(username="testRequester", password="testPassword")
        testAccount = create_user(user=testUser, first_name="John", last_name="Doe", major="CS", bio="sample")
        testRequesterAccount = create_user(user=testRequester, first_name="John", last_name="Doe", major="CS", bio="sample")
        create_buddy(testRequesterAccount, testAccount, False)
        login = self.client.force_login(testUser)
        url = reverse('userAccount:approve_buddy')
        pk = buddies.objects.all()[0].pk
        data = {'approve_item' : [pk]}
        self.client.post(url,data)
        url = reverse('userAccount:view_buddies')
        response = self.client.get(url, follow=True)
        self.assertContains(response, "No Requests Pending")