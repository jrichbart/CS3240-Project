from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from userAccount.models import userAccount, Course, Availability, buddies
from django.http import HttpResponse
from django.template import loader


def index(request):
    if(request.user.is_authenticated):
        template = loader.get_template('buddies/index.html')
        currentUser = userAccount.objects.get(user=request.user)
        courses = currentUser.courses.all()
        context = {
            'acc_name' : currentUser.name,
            'acc_major' : currentUser.major,
            'acc_bio' : currentUser.bio,
            'email' : currentUser.user.email,
            'courses' : courses,
        }
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))
