from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import userAccount, Course, Availability, buddies
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from .const_data import major_options, course_data
import json

# Create your views here.

def has_availability(request):
    if (request.user.is_authenticated):
        if (userAccount.objects.filter(user=request.user).count() > 0):
            return HttpResponseRedirect(reverse('userAccount:view_availability'))
        else:
            user = request.user
            new_account = userAccount(user=user, first_name="", last_name="")
            new_account.save()
            return HttpResponseRedirect(reverse('userAccount:view_availability'))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view availability")
        return HttpResponseRedirect(reverse('login:login'))

def view_availability(request):
    if (request.user.is_authenticated):
        currentUser = userAccount.objects.get(user=request.user)
        availability = currentUser.availability.all()
        calendar = ""
        if availability.count() > 0:
            calendar = availability[0].calendar

        template = loader.get_template('userAccount/availabilityForm.html')
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        times = []
        for i in range(8, 12):
            times.append(str(i) + ":00 AM")
        times.append("12:00 PM")
        for i in range(1,12):
            times.append(str(i) + ":00 PM")

        context = {
            'range16': range(16),
            'range7': range(7),
            'days': days,
            'times': times,
            'calendar': calendar
            }
        return HttpResponse(template.render(context, request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view availability")
        return HttpResponseRedirect(reverse('login:login'))

def save_availability(request):
    try:
        student = userAccount.objects.get(user=request.user)
        old_availability = student.availability.all()
        if old_availability.count() > 0:
            old_availability[0].delete()
            
        calendar = request.POST.get("calendar")

        availability = Availability(student=student, calendar=calendar)
        availability.save()
        messages.add_message(request, messages.SUCCESS, "Account information successfully updated")
        return HttpResponseRedirect(reverse('userAccount:view_availability'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.ERROR, "Error updating account information")
            return HttpResponseRedirect(reverse('userAccount:view_account'))
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))
    
def has_account(request):
    if(request.user.is_authenticated):
        if(userAccount.objects.filter(user=request.user).count()>0):
            return HttpResponseRedirect(reverse('userAccount:view_account'))
        else:
            user = request.user
            new_account = userAccount(user=user, first_name="", last_name="")
            new_account.save()
            return HttpResponseRedirect(reverse('userAccount:view_account'))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))

def view_account(request):
    if(request.user.is_authenticated):
        template = loader.get_template('userAccount/accountForm.html')
        currentUser = userAccount.objects.get(user=request.user)
        courses = currentUser.getCourses()

        courses_as_str = []
        for course in courses:
            courses_as_str.append(course.mnemonic + " " + course.number)

        context = {
            'acc_first_name' : currentUser.first_name,
            'acc_last_name' : currentUser.last_name,
            'acc_major' : currentUser.major,
            'acc_bio' : currentUser.bio,
            'email' : currentUser.user.email,
            'courses' : ','.join(courses_as_str),
            'major_options' : major_options,
            'course_data' : course_data
        }
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))

def save(request):
    try:
        currentUser = userAccount.objects.get(user=request.user)
        acc_first_name = request.POST.get("acc_first_name")
        acc_last_name = request.POST.get("acc_last_name")
        acc_major = request.POST.get("acc_major")
        acc_bio = request.POST.get("acc_bio")
        currentUser.first_name = acc_first_name
        currentUser.last_name = acc_last_name
        currentUser.major = acc_major
        currentUser.bio = acc_bio
        currentUser.save()

        courses_to_add = request.POST.getlist("acc_courses_added[]")
        courses_to_remove = request.POST.getlist("acc_courses_removed[]")
        all_courses = Course.objects.filter(student=currentUser)

        for delete_course in courses_to_remove:
            for course in all_courses:
                if course.mnemonic == delete_course.split(" ")[0] and course.number == delete_course.split(" ")[1]:
                    course.delete()
        
        for add_course in courses_to_add:

            # Will quietly ignore any duplicate courses
            is_duplicate = False
            for course in all_courses:
                if course.mnemonic == add_course.split(" ")[0] and course.number == add_course.split(" ")[1]:
                    is_duplicate = True

            if not is_duplicate:
                new_course = Course(student=currentUser, mnemonic=add_course.split(" ")[0], number=add_course.split(" ")[1])
                new_course.save()

        messages.add_message(request, messages.SUCCESS, "Account information successfully updated")
        return HttpResponseRedirect(reverse('userAccount:contact_info'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.ERROR, "Error updating account information")
            return HttpResponseRedirect(reverse('userAccount:view_account'))
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))

def view_buddies(request):
    if(request.user.is_authenticated):
        template = loader.get_template('userAccount/buddies.html')
        currentUser = userAccount.objects.get(user=request.user)
        buddies = currentUser.getBuddies()
        context = {
            'acc_name' : currentUser.first_name + ' ' +currentUser.last_name,
            'accepted_buddies' : buddies["accepted"],
            'pending_your_approval' : buddies["pendingYourApproval"],
            'pending_their_approval' : buddies["pendingTheirApproval"],
            'selected_buddy' : None,
        }
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view buddies")
        return HttpResponseRedirect(reverse('login:login'))

def buddy_select(request, buddy_name):
    if(request.user.is_authenticated):
        buddy = User.objects.get(username=buddy_name)
        buddy_account = userAccount.objects.get(user=buddy)
        study_buddy_list_length = len(buddy_account.getBuddies()["accepted"])
        template = loader.get_template('userAccount/buddies.html')
        currentUser = userAccount.objects.get(user=request.user)
        buddies = currentUser.getBuddies()
        shared_courses = currentUser.getSharedCourses(buddy_account)

        # Availability
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        times = []
        for i in range(8, 12):
            times.append(str(i) + ":00 AM")
        times.append("12:00 PM")
        for i in range(1,12):
            times.append(str(i) + ":00 PM")

        user_availability = Availability.objects.get(student=currentUser).calendar
        buddy_availability = Availability.objects.get(student=buddy_account).calendar
        
        context = {
            'acc_name' : currentUser.first_name + ' ' +currentUser.last_name,
            'current_user': currentUser,
            'accepted_buddies' : buddies["accepted"],
            'pending_your_approval' : buddies["pendingYourApproval"],
            'pending_their_approval' : buddies["pendingTheirApproval"],
            'denied_buddies' : buddies["denied"], 
            'selected_buddy' : buddy_account,
            'number_buddies' : study_buddy_list_length,
            'shared_courses' : shared_courses,
            'user_availability': user_availability,
            'buddy_availability': buddy_availability,
            'range16': range(16),
            'range7': range(7),
            'days': days,
            'times': times,
        }
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view buddies")
        return HttpResponseRedirect(reverse('login:login'))  

def approve_buddy(request):
    try:
        buddy_pk = request.POST.getlist('approve_item')[0]
        buddy_to_approve = userAccount.objects.get(pk=buddy_pk)
        currentUser = userAccount.objects.get(user=request.user)
        buddyObject = buddies.objects.get(requester=buddy_to_approve, requestee=currentUser)
        buddyObject.approved = True
        buddyObject.save()
        messages.add_message(request, messages.SUCCESS, "Approval successful")
        return HttpResponseRedirect(reverse('userAccount:view_buddies'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.ERROR, "Error approving request")
            return HttpResponseRedirect(reverse('userAccount:view_buddies'))
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))

def deny_buddy(request):
    try:
        buddy_pk = request.POST.getlist('deny_item')[0]
        buddy_to_approve = userAccount.objects.get(pk=buddy_pk)
        currentUser = userAccount.objects.get(user=request.user)
        buddyObject = buddies.objects.get(requester=buddy_to_approve, requestee=currentUser)
        buddyObject.denied = True
        buddyObject.save()
        messages.add_message(request, messages.SUCCESS, "Approval denied")
        return HttpResponseRedirect(reverse('userAccount:view_buddies'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.ERROR, "Error denying request")
            return HttpResponseRedirect(reverse('userAccount:view_buddies'))
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))

def contact_info(request):
    if(request.user.is_authenticated):
        template = loader.get_template('userAccount/contactInfo.html')
        currentUser = userAccount.objects.get(user=request.user)
        context = {
            'computing_id' : currentUser.computing_id,
            'phone_number' : currentUser.phone_number,
            'discord_name' : currentUser.discord_name,
        }
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to edit contact info")
        return HttpResponseRedirect(reverse('login:login'))

def save_contact(request):
    try:
        currentUser = userAccount.objects.get(user=request.user)
        computing_id = request.POST.get("computing_id")
        phone_number = request.POST.get("phone_number")
        discord_name = request.POST.get("discord_name")
        currentUser.computing_id = computing_id
        currentUser.phone_number = phone_number
        currentUser.discord_name = discord_name
        currentUser.save()
        messages.add_message(request, messages.SUCCESS, "Contact information successfully updated")
        return HttpResponseRedirect(reverse('userAccount:contact_info'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.ERROR, "Error updating contact information")
            return HttpResponseRedirect(reverse('userAccount:contact_info'))
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view contact information")
            return HttpResponseRedirect(reverse('login:login'))