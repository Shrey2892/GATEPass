from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponseForbidden
from .models import User
from mongoengine import NotUniqueError,DoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.

def register(request):
    error_message = None
    #  template = loader.get_template('pages-register.html')
    #  return HttpResponse(template.render())
    # return render (request,'pages-register.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        terms_accepted = 'terms' in request.POST
    
        if not all([name, email, username, password]):
            error_message = "All fields are required!"
        
        else:
        
            # Check for existing user
            if User.objects(username=username).first() or User.objects(email=email).first():
                error_message = "Username or email already exists!"
        
        
        # Create and save a new user
    
            else:
                user = User(
                      name=name,
                      email=email,
                      username=username,
                      password=password,
                      terms_accepted=terms_accepted
                )
                try:
                    user.save()  # Save to MongoDB
                    return redirect('login')  # Redirect after successful registration
                except NotUniqueError:
                    error_message = "Username or email already exists!"
                

    return render(request, 'pages-register.html', {'error_message': error_message})
    


def login(request):
    #  template = loader.get_template('pages-login.html')
    #  return HttpResponse(template.render())
    # 
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            error_message = "Both fields are required."
        else:
            try:
                # Retrieve the user from the database
                user = User.objects.get(username=username)
                
                # Check if the password matches
                if user.password == password:  # Use proper password hashing in production
                    # Log the user in (you might set a session or a cookie here)
                    request.session['user_id'] = str(user.id)
                    return redirect('home')  # Redirect to a home or dashboard page
                else:
                    error_message = "Invalid password."
            except DoesNotExist:
                error_message = "User does not exist."

    return render(request, 'pages-login.html', {'error_message': error_message})





def home(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login') 
    try:
       user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')
    
    return render(request,'pages-home.html',{'user': user})

