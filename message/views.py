from django.shortcuts import render
from django.http import HttpResponse

from message.models import  DemandColumnInfo

# Create your views here.

def getform(request):
     context = {}
     context['hello'] = 'Hello World!'
     return render(request, 'temp.html', context)

def getHellworld(request):
     return HttpResponse('hello world')

def login(request):
     pass