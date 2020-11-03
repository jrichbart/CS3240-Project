from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from userAccount.models import userAccount, Course, Availability, buddies
from django.http import HttpResponse
from django.template import loader


def index(request):
    latest_account_list = userAccount.objects.all()
    context = {'latest_account_list': latest_account_list}
    return render(request, 'buddies/index.html', context)
