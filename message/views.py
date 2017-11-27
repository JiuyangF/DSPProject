from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def getform(request):
     context          = {}
     context['hello'] = 'Hello World!'
     return render(request, 'temp.html', context)

def getHellworld():
     infmation = ''
     pass