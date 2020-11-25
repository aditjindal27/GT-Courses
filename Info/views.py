from django.shortcuts import render
from Info.models import *
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home_info.html')

def getInfo(request):
    inp = request.POST['className']
    className = inp.strip().upper()
    x = Oscar(className)

    return render(request, 'result2.html', {'obj': x})