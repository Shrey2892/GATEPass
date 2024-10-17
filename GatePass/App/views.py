from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import User
# Create your views here.

def register(request):
    #  template = loader.get_template('pages-register.html')
    #  return HttpResponse(template.render())
    return render (request,'pages-register.html')


def login(request):
    #  template = loader.get_template('pages-login.html')
    #  return HttpResponse(template.render())
    return render(request,'pages-login.html')


def user_form(request):
    print(request.POST)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', "")
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        # Check if a user with the same username exists
        user = User.objects(username=username).first()
        if user is None:
            # Create a new user document if it doesn't exist
            user = User(username=username)

        # Update fields with submitted data
        user.pwd = pwd
        user.email = email
        user.name = name

        user.save()  # Save the user to MongoDB
        return redirect('login')  # Redirect to a success page

    return render(request, 'myapp/pages-login.html')