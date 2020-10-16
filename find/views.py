from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User

def index(request):
    latest_account_list = User.objects.order_by('-username')[:5]
    context = {'latest_account_list': latest_account_list}
    return render(request, 'find/index.html', context)