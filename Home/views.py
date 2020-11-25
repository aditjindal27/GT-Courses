from django.shortcuts import render
from django.http import HttpResponse
from Home.models import Course_Critique, RateMyProfScraper
# Create your views here.

def home(request):
    return render(request, 'home.html')

def getClass(request):


    inp = request.POST['className']
    x = Course_Critique(inp)
    x.className = inp

    y = RateMyProfScraper(361)
    y.helper(x.dic)

    z = zip(x.oprofs, x.ogpas, y.final, y.links)

    return render(request, 'result.html', {'obj': x, 'z': z})

