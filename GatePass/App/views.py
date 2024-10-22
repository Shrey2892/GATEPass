from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponseForbidden,HttpResponse,JsonResponse
from .models import User,Gatepass,Receipt
from mongoengine import NotUniqueError,DoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Gatepass
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

# def form(request):
#     return render(request,'pages-form.html')
    

def form(request):
    
    if request.method == 'POST':

    #     visitor_name = request.POST.get('visitor_name')
    #     purpose = request.POST.get('purpose')
    #     created_at = request.POST.get('created_at')

    #     print(f"Visitor Name: {visitor_name}, Purpose: {purpose}")  # Debugging line
    #     gatepass = Gatepass(
    #         visitor_name=visitor_name, 
    #         purpose=purpose, 
    #         created_at=datetime.now()
    #     )
    #     gatepass.save()
    #     return redirect('main')
    # return render(request, 'pages-form.html')
        
        driver_name = request.POST.get('driver_name')
        purpose = request.POST.get('purpose')
        gatepassno =request.POST.get('gatepassno')
        vehicle_number=request.POST.get('vehicle_number')
        owner_contact_no=request.POST.get('owner_contact_no')
        Access_Area=request.POST.get('Access_Area')
        token=request.POST.get('token')
        Restricted_Area=request.POST.get('Restricted_Area')
       

       
        errors = {}
        if not driver_name:
            errors['Driver Name'] = 'Visitor name is required.'
        if not purpose:
            errors['Purpose'] = 'Purpose is required.'
        if not gatepassno:
            errors['Gate Pass No'] = 'GatePass No. should be allocated.'
        
        if not vehicle_number:
            errors['vehicle Number'] = 'Vehicle number is required.'
        
        if not owner_contact_no:
            errors['Contact Number'] = 'Conatct number  is required.'

        if not Access_Area:
            errors['Access Area'] = 'Access Area needs to be allocated.'

        if not token:
            errors['Token'] ='Please Generate Token.'

        if Gatepass.objects(token=token).first():
            errors['Token'] = "Token already allotted."
        
        if Gatepass.objects(gatepassno=gatepassno).first():
            errors['Gate Pass No.'] = "GatePass No. already Exists"

        if len(owner_contact_no) !=10:
            errors['Contact No'] = "Phone number must be 10 digit."
        
        if errors:
            # Re-render the form with errors if validation fails
            return render(request, 'pages-form.html', {
                'errors': errors,
                'driver_name':driver_name,
                'purpose': purpose,
                'gatepassno':gatepassno,
                'vehicle_number':vehicle_number,
                'owner_contact_no':owner_contact_no,
                'Access_Area':Access_Area,
                'token':token,
                'Restricted_Area':Restricted_Area
                
            })
        
        try:
            gatepass = Gatepass(
                gatepassno=gatepassno,
                vehicle_number=vehicle_number,
                owner_contact_no=owner_contact_no,
                driver_name=driver_name,
                purpose=purpose,
                Access_Area=Access_Area,
                Restricted_Area=Restricted_Area,
                token=token,
                created_at=datetime.now(),
                
                  # Use current timestamp
            )
            
            gatepass.save()  # Save to MongoDB
            return redirect('receipt', gatepass_id=gatepass.id)  #Redirect after success
        except Exception as e:
            errors['database'] = str(e)
            return render(request, 'pages-form.html', {
                'errors': errors,
                'gatepassno':gatepassno,
                'vehicle_number':vehicle_number,
                'driver_name': driver_name,
                'purpose': purpose,
                'Access_Area':Access_Area,
                'token':token,
                'Restricted_Area':Restricted_Area,

                
            })
     
    return render(request,'pages-form.html')

    

       
       
       
       
       
       
       
       
       
        # form = Gatepass(request.POST)
#         if form.is_valid():
            
#             # Create a new Gatepass document using keyword arguments
#             form = Gatepass(
            
#                 visitor_name=form.cleaned_data['visitor_name'],
#                 purpose=form.cleaned_data['purpose'],
#                 created_at=form.cleaned_data.get('created_at', datetime.now())  # Default to now if not provided
#             )
#             form.save()  # Save to MongoDB
#             return redirect('home')  # Redirect after success
#    else:
#         form = Gatepass()  # Initialize a new form instance for GET request

#    return render(request, 'pages-form.html', {'form': form}) 
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    # user_id = request.session.get('user_id')

        

    # if not user_id:
    #     return redirect('login') 
    # try:
    #    user = User.objects.get(id=user_id)
       
    # except User.DoesNotExist:

    #     return redirect('login')
    
    # if request.method == 'POST':
    #     form = Gatepass(request.POST)
    #     if form.is_valid():
    #         # Create a new Gatepass document
    #         user_data = Gatepass(
    #             visitor_name=form.cleaned_data['visitor_name'],
    #             purpose=form.cleaned_data['purpose'],
    #             created_at=form.cleaned_data['created_at']
    #         )
    #         user_data.save()  # Save to MongoDB
    #         return redirect('home')  # Redirect after success
    # else:
    #     form = Gatepass() 
    
    # return render(request,'pages-form.html',{'form': form, 'user': user})
    

def index(request):
    template = loader.get_template('pages-index.html')
    return HttpResponse(template.render())
    # return render (request,'pages-index.html')

    # return render(request,'pages-index.html')


def logout_view(request):
    # Clear session data
    logout(request)  # This will clear the session
    
    # Add any additional actions here
    return redirect('login')  


# def submit_form(request):
#     if request.method == 'POST':
#         form = Gatepass(request.POST)
#         if form.is_valid():
#             # Create a new UserForm document
#             user_data = Gatepass(
#                 visitor_name= form.cleaned_data['visitor_name'],
#                 purpose=form.cleaned_data['purpose'],
#                 created_at=form.cleaned_data['created_at']
#             )
#             user_data.save()  # Save to MongoDB
#             return redirect('home')  # Redirect after success
#         else:
#             form = Gatepass()

#     return render(request, 'pages-form.html', {'form': form})

def receipt(request,gatepass_id ):    #gatepass_id
    gatepass = Gatepass.objects.get(id=gatepass_id)
    return render(request, 'receipt.html', {'gatepass': gatepass})

    # receipt = get_object_or_404(Receipt.objects, id=id)
    # return render(request, 'print_receipt.html', {'receipt': receipt})



def edit_gatepass_view(request, token):
    # Retrieve the existing GatePass entry
    gatepass = get_object_or_404(Gatepass, token=token)

    if request.method == 'POST':
        # Update the fields with the submitted data
        gatepass.gatepassno = request.POST.get('gatepassno', gatepass.gatepassno)
        gatepass.vehicle_number = request.POST.get('vehicle_number', gatepass.vehicle_number)
        gatepass.driver_name = request.POST.get('driver_name', gatepass.driver_name)
        gatepass.owner_contact_no = request.POST.get('owner_contact_no', gatepass.owner_contact_no)
        gatepass.purpose = request.POST.get('purpose', gatepass.purpose)
        gatepass.Access_Area = request.POST.get('Access_Area', gatepass.Access_Area)
        gatepass.Restricted_Area = request.POST.get('Restricted_Area', gatepass.Restricted_Area)

        errors = {}

        # Validate the fields
        if not gatepass.gatepassno:
            errors['gatepassno'] = "Gate Pass No is required."
        if not gatepass.token:
            errors['token'] = "Token is required."
        if not gatepass.vehicle_number:
            errors['vehicle_number'] = "Vehicle Number is required."
        if not gatepass.driver_name:
            errors['driver_name'] = "Driver Name is required."
        if not gatepass.owner_contact_no:
            errors['owner_contact_no'] = "Contact No is required."
        if not gatepass.purpose:
            errors['purpose'] = "Purpose is required."
        if not gatepass.Access_Area:
            errors['Access_Area'] = "Access Area is required."
        if not gatepass.Restricted_Area:
            errors['Restricted_Area'] = "Restricted Area is required."

        # Check for existing token
        if Gatepass.objects(token=gatepass.token).exclude(id=gatepass.id).first():
            errors['token'] = "Token already allotted."

        if not errors:
            # Save the updated GatePass
            gatepass.save()
            return redirect('receipt')  # Redirect after successful update

    return render(request, 'pages-form.html', {
        'errors': errors,
        'gatepassno': gatepass.gatepassno,
        'token': gatepass.token,
        'vehicle_number': gatepass.vehicle_number,
        'driver_name': gatepass.driver_name,
        'owner_contact_no': gatepass.owner_contact_no,
        'purpose': gatepass.purpose,
        'Access_Area': gatepass.Access_Area,
        'Restricted_Area': gatepass.Restricted_Area
    })


def delete_form(request):
    gatepassno = request.GET.get('gatepassno')
    gate_pass = Gatepass.objects(gatepassno=gatepassno).first()

    if gate_pass:
        data = {
            'token': gate_pass.token,
            'vehicle_number': gate_pass.vehicle_number,
            'driver_name': gate_pass.driver_name,
            'owner_contact_no': gate_pass.owner_contact_no,
            'purpose': gate_pass.purpose,
            'Access_Area': gate_pass.Access_Area,
            'Restricted_Area': gate_pass.Restricted_Area,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Gate pass not found'}, status=404)