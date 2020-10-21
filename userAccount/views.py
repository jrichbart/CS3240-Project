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
        context = {
            'acc_name' : currentUser.name,
            'email' : currentUser.user.email
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

def class_form(request):
    if(request.user.is_authenticated):
        template = loader.get_template('userAccount/classForm.html')
        context = {}
        return HttpResponse(template.render(context,request))
    else:
        messages.add_message(request, messages.ERROR, "Login before attempting to view account")
        return HttpResponseRedirect(reverse('login:login'))

def add_class(request):
    try:
        student = userAccount.objects.get(user=request.user)
        mnemonic = request.POST.get("course_mnemonic")
        number = request.POST.get("course_number")
        newCourse = Course(student=student, mnemonic=mnemonic, number=number)
        newCourse.save()
        messages.add_message(request, messages.SUCCESS, "Class added successfully")
        return HttpResponseRedirect(reverse('userAccount:view_account'))
    except:
        if(request.user.is_authenticated):
            messages.add_message(request, messages.SUCCESS, "Class not added")
            return render(request, 'userAccount/accountForm.html')
        else:
            messages.add_message(request, messages.ERROR, "Login before attempting to view account")
            return HttpResponseRedirect(reverse('login:login'))