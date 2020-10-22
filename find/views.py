from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from userAccount.models import userAccount

def index(request):
    latest_account_list = userAccount.objects.all()
    context = {'latest_account_list': latest_account_list}
    return render(request, 'find/index.html', context)