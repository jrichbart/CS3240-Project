from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import userAccount, Course
from django.template import loader
from django.contrib import messages

# Create your views here.

def has_account(request):
    if(request.user.is_authenticated):
        if(userAccount.objects.filter(user=request.user).count()>0):
            return HttpResponseRedirect(reverse('userAccount:view_account'))
        else:
            user = request.user
            name = ""
            new_account = userAccount(user=user, name=name)
            new_account.save()
            return HttpResponseRedirect(reverse('userAccount:view_account'))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))

def view_account(request):
    if(request.user.is_authenticated):
        template = loader.get_template('userAccount/accountForm.html')
        currentUser = userAccount.objects.get(user=request.user)
        courses = currentUser.courses.all() 
        context = {
            'acc_name' : currentUser.name,
            'email' : currentUser.user.email,
            'courses' : courses,
        }
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))

def save(request):
    try:
        currentUser = userAccount.objects.get(user=request.user)
        acc_name = request.POST.get("acc_name")
        currentUser.name = acc_name
        currentUser.save()
        messages.add_message(request, messages.SUCCESS, "Account information successfully updated")
        return HttpResponseRedirect(reverse('userAccount:view_account'))
    except:
        if(request.user.is_authenticated):
            return render(request, 'userAccount/accountForm.html')
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))

def course_form(request):
    if(request.user.is_authenticated):
        template = loader.get_template('userAccount/courseForm.html')
        context = {}
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))

def add_course(request):
    try:
        student = userAccount.objects.get(user=request.user)
        mnemonic = request.POST.get("course_mnemonic")
        number = request.POST.get("course_number")
        if (len(number)!=4 or len(mnemonic) < 2 or len(mnemonic) > 4):
            messages.add_message(request, messages.ERROR, "Incorrect course format")
            return HttpResponseRedirect(reverse('userAccount:view_account'))

        newCourse = Course(student=student, mnemonic=mnemonic, number=number)
        newCourse.save()
        messages.add_message(request, messages.SUCCESS, "Course added successfully")
        return HttpResponseRedirect(reverse('userAccount:view_account'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.SUCCESS, "Course was not added")
            return HttpResponseRedirect(reverse('userAccount:view_account'))
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))

def delete_course(request):
    pass