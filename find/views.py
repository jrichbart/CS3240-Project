from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from userAccount.models import userAccount, Course, Availability, buddies, Message
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

    user_buddies_requester = buddies.objects.filter(requester=user_account)
    user_buddies_requestee = buddies.objects.filter(requestee=user_account)
    user_buddy_names = set()
    for buddy in user_buddies_requester:
        user_buddy_names.add(buddy.requestee.user)

    for buddy in user_buddies_requestee:
        user_buddy_names.add(buddy.requester.user)

    latest_account_list = userAccount.objects.all()
    latest_account_list_as_dict = []
    for account in latest_account_list:
        if account.user == request.user or account.user in user_buddy_names:
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
        a['raw_availability'] = account_availability
        latest_account_list_as_dict.append(a)

    # Sort each buddy's courses
    for buddy in latest_account_list_as_dict:
        buddy['courses'] = sorted(buddy['courses'], key=lambda c: c['mnemonic'])

    # Availability
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    times = []
    for i in range(8, 12):
        times.append(str(i) + ":00 AM")
    times.append("12:00 PM")
    for i in range(1,12):
        times.append(str(i) + ":00 PM")

    context = {
        'filtered_buddy_list': latest_account_list_as_dict,
        'userAccount': user_account,
        'userCourses': user_courses_as_dict,
        'userAvailability': user_availability,
        'range16': range(16),
        'range7': range(7),
        'days': days,
        'times': times,
        }
    return HttpResponse(template.render(context, request))

def get_availability_string(u, a):
    if u == "" or a == "" or len(u) != len(a):
        return "No Availability Data"
    else:
        matches = 0
        available = 0
        for i in range(len(u)):
            if u[i] == "X":
                available += 1
                if u[i] == a[i]:
                    matches += 1
        return str(int(100 * matches / available)) + "% Availability Match"

def view_send_request(request, user):
    template = loader.get_template('find/buddyRequestForm.html')
    requester = userAccount.objects.get(user=request.user)

    # Redirect to find page if the requester already has a buddy relationship
    # with this user
    user_buddies_requester = buddies.objects.filter(requester=requester)
    user_buddies_requestee = buddies.objects.filter(requestee=requester)
    user_buddy_names = set()
    for buddy in user_buddies_requester:
        user_buddy_names.add(str(buddy.requestee.user))

    for buddy in user_buddies_requestee:
        user_buddy_names.add(str(buddy.requester.user))

    if user in user_buddy_names:
        return HttpResponseRedirect(reverse('find:index'))

    buddy = User.objects.get(username=user)
    requestee = userAccount.objects.get(user=buddy) 
    context = {
        "requestee_first_name": requestee.first_name,
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

    message = Message(unread=True, content=request_message, sequence=1, from_requester=True, buddies=new_buddy_request)
    message.save()
    return HttpResponseRedirect(reverse('find:index'))