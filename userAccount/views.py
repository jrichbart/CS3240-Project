from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def availability(request):
    template = loader.get_template('userAccount/availability.html')
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    times = []
    for i in range(8, 12):
        times.append(str(i) + ":00 AM")
    times.append("12:00 PM")
    for i in range(1,12):
        times.append(str(i) + ":00 PM")

    context = {'range16': range(16), 'range7': range(7), 'days': days, 'times': times}
    return HttpResponse(template.render(context, request))