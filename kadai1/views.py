from django. shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("ようこそ")

def login(request):
    return render(request,'index.html')