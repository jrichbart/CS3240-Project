from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import userAccount
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
    template = loader.get_template('userAccount/accountForm.html')
    currentUser = userAccount.objects.get(user=request.user)
    context = {
        'acc_name' : currentUser.name,
        'email' : currentUser.user.email
    }
    return HttpResponse(template.render(context,request))

def save(request):
    try:
        currentUser = userAccount.objects.get(user=request.user)
        acc_name = request.POST.get("acc_name")
        currentUser.name = acc_name
        currentUser.save()
        messages.add_message(request, messages.SUCCESS, "Account information successfully updated")
        return HttpResponseRedirect(reverse('userAccount:view_account'))
    except:
        return render(request, 'userAccount/accountForm.html')