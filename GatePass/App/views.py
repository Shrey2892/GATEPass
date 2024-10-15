from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def register(request):
    #  template = loader.get_template('pages-register.html')
    #  return HttpResponse(template.render())
    return render (request,'pages-register.html')


def login(request):
    #  template = loader.get_template('pages-login.html')
    #  return HttpResponse(template.render())
    return render(request,'pages-login.html')




