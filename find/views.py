from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from userAccount.models import userAccount, Course, Availability, buddies
from django.urls import reverse

def index(request):

    template = loader.get_template('find/index.html')

    if (userAccount.objects.filter(user=request.user).count() > 0):
        user_account = userAccount.objects.get(user=request.user)
    else:
        return HttpResponseRedirect(reverse('login:home'))

    user_courses = Course.objects.filter(student=user_account)
    user_courses = sorted(user_courses, key=lambda c: c.mnemonic)
    try:
        user_availability = Availability.objects.get(student=user_account).calendar
    except:
        user_availability = ""

    # Convert courses to dicts
    user_courses_as_dict = []
    for course in user_courses:
        c = {}
        c['mnemonic'] = course.mnemonic
        c['number'] = course.number
        user_courses_as_dict.append(c)

    latest_account_list = userAccount.objects.all()
    latest_account_list_as_dict = []
    for account in latest_account_list:
        if account.user == request.user:
            continue

        account_user = userAccount.objects.get(user=account.user)
        account_courses = Course.objects.filter(student=account_user)
        account_courses_as_dict = []
        match_found = False

        for course in account_courses:
            _c = {}
            _c['mnemonic'] = course.mnemonic
            _c['number'] = course.number
            if _c in user_courses_as_dict:
                match_found = True
            account_courses_as_dict.append(_c)

        # If no courses match the user's, disregard this account
        if not match_found:
            continue

        # Get availability
        try:
            account_availability = Availability.objects.get(student=account_user).calendar
        except:
            account_availability = ""


        a = {}
        a['user'] = account_user
        a['firstName'] = account.first_name
        a['lastName'] = account.last_name
        a['major'] = account.major
        a['bio'] = account.bio
        a['numBuddies'] = 0
        a['courses'] = account_courses_as_dict
        a['availability_string'] = get_availability_string(user_availability, account_availability)
        latest_account_list_as_dict.append(a)

    # Sort each buddy's courses
    for buddy in latest_account_list_as_dict:
        buddy['courses'] = sorted(buddy['courses'], key=lambda c: c['mnemonic'])

    context = {
        'filtered_buddy_list': latest_account_list_as_dict,
        'userAccount': user_account,
        'userCourses': user_courses_as_dict
        }
    return HttpResponse(template.render(context, request))

def get_availability_string(u, a):
    if u == "" or a == "" or len(u) != len(a):
        return "No Availability Data"
    else:
        matches = 0
        for i in range(len(u)):
            if u[i] == a[i]:
                matches += 1
        return str(int(100 * matches / len(u))) + "% Availability Match"

def view_send_request(request, user):
    template = loader.get_template('find/buddyRequest.html')
    buddy = User.objects.get(username=user)
    requestee = userAccount.objects.get(user=buddy) 
    context = {
        "requestee_name": requestee.first_name + " " + requestee.last_name,
        "requestee_username": requestee.user
    }
    return HttpResponse(template.render(context, request))


def send_buddy_request(request, user):
    current_user = userAccount.objects.get(user=request.user)
    buddy = User.objects.get(username=user)
    requestee = userAccount.objects.get(user=buddy) 

    request_message = request.POST.get("request_message_input")

    new_buddy_request = buddies(requester=current_user, requestee=requestee, request_message=request_message, approved=False, denied_message="", denied=False)
    new_buddy_request.save()
    return index(request)