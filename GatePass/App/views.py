from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponseForbidden,HttpResponse,JsonResponse
from .models import User,Gatepass,Receipt,Outpass
from mongoengine import NotUniqueError,DoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Gatepass
from bson import ObjectId
from mongoengine import DoesNotExist
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
        existing_gatepass = None
        existing_outpass = None
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
            # Check if the token already exists in the Gatepass model
            print(f"Received token: {token}")
        existing_gatepass = Gatepass.objects(token=token).first()
        if existing_gatepass:
            errors['Token'] = "Token already allotted in Gatepass."
        
        if not existing_gatepass:
            existing_outpass = Outpass.objects.filter(token=token).first()
            if existing_outpass:
                # Delete existing Outpass to allow reuse of the token
                existing_outpass.delete()

        # Check if the token exists in the Outpass model
        # existing_outpass = Outpass.objects(token=token).first()
        # if existing_outpass:
        #     # Allow reuse of token from Outpass, so no error here
        #     existing_outpass.delete()
        # if Gatepass.objects(token=token).first():
        #     errors['Token'] = "Token already allotted in Gatepass."

        # # Check if the token exists in the Outpass model
        # if Outpass.objects(token=token).first():
        #     # Allow reuse of token from Outpass, so don't add an error
        #     pass

        # if Gatepass.objects(token=token).first():
            
        #     errors['Token'] = "Token already allotted."
        # if existing_outpass and existing_gatepass:
        #     existing_outpass.delete()


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






def request_out_pass(request):
    
    # if request.method == 'POST':
    #     gatepassno = request.POST.get('gatepassno')

    #     # Try to retrieve the Gatepass data
    #     try:
    #         gatepass = Gatepass.objects.get(gatepassno=gatepassno)
    #     except Gatepass.DoesNotExist:
    #         return render(request, 'request_out_pass.html', {'error': 'Gate pass not found.'})

    #     # Save the data to the Outpass model
    #     out_pass = Outpass(
    #         gatepassno=gatepass.gatepassno,
    #         token=gatepass.token,
    #         vehicle_number=gatepass.vehicle_number,
    #         driver_name=gatepass.driver_name,
    #         owner_contact_no=gatepass.owner_contact_no,
    #         purpose=gatepass.purpose,
    #         Access_Area=gatepass.Access_Area,
    #         Restricted_Area=gatepass.Restricted_Area
    #     )
    #     out_pass.save()  # Save the instance to the Outpass model

    #     # Redirect to success page with gatepassno
    #     return redirect('out_pass_success', gatepassno=gatepassno)

    # return render(request, 'request_out_pass.html',)
    if request.method == 'POST':
        gatepassno = request.POST.get('gatepassno')

        # Try to retrieve the Gatepass data
        try:
            gatepass = Gatepass.objects.get(gatepassno=gatepassno)
        except Gatepass.DoesNotExist:
            return render(request, 'request_out_pass.html', {'error': 'Gate pass not found.'})

        # Check if an Outpass with the same gatepassno already exists
        existing_outpass = Outpass.objects.filter(gatepassno=gatepassno).first()
        if existing_outpass:
            return render(request, 'request_out_pass.html', {'error': 'An out pass already exists for this gate pass number.'})

        # Save the data to the Outpass model
        out_pass = Outpass(
            gatepassno=gatepass.gatepassno,
            token=gatepass.token,
            vehicle_number=gatepass.vehicle_number,
            driver_name=gatepass.driver_name,
            owner_contact_no=gatepass.owner_contact_no,
            purpose=gatepass.purpose,
            Access_Area=gatepass.Access_Area,
            Restricted_Area=gatepass.Restricted_Area
        )
        out_pass.save()  # Save the instance to the Outpass model

        # Redirect to success page with gatepassno
        return redirect('out_pass_success', gatepassno=gatepassno)

    return render(request, 'request_out_pass.html')


def fetch_out_pass(request):
    gatepassno = request.GET.get('gatepassno')
    print(f"Received gatepassno: {gatepassno}") 
    try:
        out_pass = Gatepass.objects.get(gatepassno=gatepassno)
        data = {
            'token': out_pass.token,
            'vehicle_number':out_pass.vehicle_number,
            'driver_name':out_pass.driver_name,
            'owner_contact_no':out_pass.owner_contact_no,
            'purpose': out_pass.purpose,
            'Access_Area':out_pass.Access_Area,
            'Restricted_Area':out_pass.Restricted_Area,
            # 'created_At': out_pass.created_at.strftime('%Y-%m-%dT%H:%M'),  # Format for datetime-local
        }
        return JsonResponse(data)  
    except Outpass.DoesNotExist:
        return JsonResponse({'error': 'Out pass not found.'}, status=404)
    
def display_outpass(request, gatepassno):
    # outpass = get_object_or_404(Outpass, gatepassno=gatepassno)
    # return render(request, 'out_pass_success.html', {'outpass': outpass})
     outpass =Outpass.objects.get(id=gatepassno)
     return render(request,'out_pass_success.html',{'outpass':outpass})

    # gatepass = Gatepass.objects.get(id=gatepass_id)
    # return render(request, 'receipt.html', {'gatepass': gatepass})




    # try:
    #     gatepass = Gatepass.objects.get(gatepassno=gatepassno)
    # except DoesNotExist:
    #     return render(request, '404.html')  # Or any other error handling
    # # gatepass = get_object_or_404(Gatepass, gatepassno=gatepassno)

    # if request.method == 'POST':
    #     # Get updated data from the form
    #     gatepass.driver_name = request.POST.get('driver_name')
    #     gatepass.purpose = request.POST.get('purpose')
    #     gatepass.vehicle_number = request.POST.get('vehicle_number')
    #     gatepass.owner_contact_no = request.POST.get('owner_contact_no')
    #     gatepass.Access_Area = request.POST.get('Access_Area')
    #     gatepass.token = request.POST.get('token')
    #     gatepass.Restricted_Area = request.POST.get('Restricted_Area')

    #     # Save updated gatepass
    #     gatepass.save()
    #     return redirect('out_pass_update', gatepassno=gatepass.gatepassno)

    # return render(request, 'edit_out_pass.html', {'gatepass': gatepass})


#try update logic
def update_gatepass(request, gatepassno):
    try:
        gatepass = Gatepass.objects.get(gatepassno=gatepassno)
    except DoesNotExist:
        return render(request, '404.html')  # Render a 404 page if not found

    if request.method == 'POST':
        # Directly update fields from the POST request
        # gatepass.user_name = request.POST.get('user_name', gatepass.user_name)
        # gatepass.date_issued = request.POST.get('date_issued', gatepass.date_issued)
        # gatepass.purpose = request.POST.get('purpose', gatepass.purpose)
        gatepass.gatepassno = request.POST.get('gatepassno')
        gatepass.driver_name = request.POST.get('driver_name')
        gatepass.purpose = request.POST.get('purpose')
        gatepass.vehicle_number = request.POST.get('vehicle_number')
        gatepass.owner_contact_no = request.POST.get('owner_contact_no')
        gatepass.Access_Area = request.POST.get('Access_Area')
        gatepass.token = request.POST.get('token')
        gatepass.Restricted_Area = request.POST.get('Restricted_Area')

        # Save the updated document
        gatepass.save()
        return redirect('update_success_page', gatepassno=gatepass.gatepassno)  # Redirect to a success page or list

    return render(request, 'update_gatepass.html', {'gatepass': gatepass})

def update_success_page(request,gatepassno):

    # gatepass = get_object_or_404(Gatepass, gatepassno=gatepassno)
    try:
        # Fetch the Gatepass instance using MongoEngine
        gatepass = Gatepass.objects.get(gatepassno=gatepassno)
    except DoesNotExist:
        return render(request, '404.html')  # Handle not found
    context = {'gatepass': gatepass}
    return render(request,'update_success_page.html',context)


def update_outpass(request, gatepassno):
    try:
        out_pass = Outpass.objects.get(gatepassno=gatepassno)
    except DoesNotExist:
        return render(request, '404.html')  # Render a 404 page if not found

    if request.method == 'POST':
        # Directly update fields from the POST request
        # gatepass.user_name = request.POST.get('user_name', gatepass.user_name)
        # gatepass.date_issued = request.POST.get('date_issued', gatepass.date_issued)
        # gatepass.purpose = request.POST.get('purpose', gatepass.purpose)
        out_pass.gatepassno = request.POST.get('gatepassno')
        out_pass.driver_name = request.POST.get('driver_name')
        out_pass.purpose = request.POST.get('purpose')
        out_pass.vehicle_number = request.POST.get('vehicle_number')
        out_pass.owner_contact_no = request.POST.get('owner_contact_no')
        out_pass.Access_Area = request.POST.get('Access_Area')
        out_pass.token = request.POST.get('token')
        out_pass.Restricted_Area = request.POST.get('Restricted_Area')

        # Save the updated document
        out_pass.save()
        return redirect('update_outpass_success_page', gatepassno=out_pass.gatepassno)  # Redirect to a success page or list

    return render(request, 'update_outpass.html', {'outpass': out_pass})

def update_outpass_success_page(request,gatepassno):

    # gatepass = get_object_or_404(Gatepass, gatepassno=gatepassno)
    try:
        # Fetch the Gatepass instance using MongoEngine
        out_pass = Outpass.objects.get(gatepassno=gatepassno)
    except DoesNotExist:
        return render(request, '404.html')  # Handle not found
    context = {'outpass': out_pass}
    return render(request,'update_outpass_success_page.html',context)

def out_pass_success(request,gatepassno):
    # out_pass = get_object_or_404(Gatepass, gatepassno=gatepassno)
    
    # return render(request, 'out_pass_success.html',{'out_pass': out_pass})
   
    try:
        # Fetch the Outpass instance based on gatepassno
        out_pass = Outpass.objects.get(gatepassno=gatepassno)
        return render(request, 'out_pass_success.html', {'out_pass': out_pass})
    except Outpass.DoesNotExist:
        return render(request, 'error.html', {'error': 'Out pass not found.'})
   
    
    # return render(request, 'out_pass_success.html', {'gatepassno': gatepassno})

def delete_gatepass(request):
    if request.method == 'POST':
        # Get the gatepass number from the form
        gatepass_no = request.POST.get('gatepassno')
        
        # Fetch the Gatepass object based on the gatepass number
        # gatepass = get_object_or_404(Gatepass, gatepassno=gatepass_no)
        
        # # Delete the Gatepass object
        # gatepass.delete()
        
        # # Redirect to a success page or wherever you need
        # return redirect('form')  # Replace with your success URL
        try:
            gatepass = Gatepass.objects.get(gatepassno=gatepass_no)
            gatepass.delete()  # Delete the Gatepass object
            return redirect('home')  # Redirect to a success page
        except Gatepass.DoesNotExist:
            # Handle the case where the gatepass number does not exist
            return render(request, 'delete_gatepass_form.html', {
                'error': 'Gatepass not found.'
            })
    
    return render(request, 'delete_gatepass_form.html')

def delete_outpass(request):
    if request.method == 'POST':
        # Get the gatepass number from the form
        gatepass_no = request.POST.get('gatepassno')
        
        # Fetch the Gatepass object based on the gatepass number
        # gatepass = get_object_or_404(Gatepass, gatepassno=gatepass_no)
        
        # # Delete the Gatepass object
        # gatepass.delete()
        
        # # Redirect to a success page or wherever you need
        # return redirect('form')  # Replace with your success URL
        try:
            outpass = Outpass.objects.get(gatepassno=gatepass_no)
            outpass.delete()  # Delete the Gatepass object
            return redirect('home')  # Redirect to a success page
        except Gatepass.DoesNotExist:
            # Handle the case where the gatepass number does not exist
            return render(request, 'delete_outpass_form.html', {
                'error': 'Outpass not found.'
            })
    
    return render(request, 'delete_outpass_form.html')


def find_gatepass(request):
    gatepass = None  # Initialize variable to hold the found gatepass
    error = None  # Variable to hold any error messages

    if request.method == 'POST':
        gatepass_no = request.POST.get('gatepassno')

        # Try to fetch the Gatepass from the database
        try:
            gatepass = Gatepass.objects.get(gatepassno=gatepass_no)
        except Gatepass.DoesNotExist:
            error = 'Gatepass not found. Please check the Gatepass number and try again.'

    return render(request, 'find_gatepass.html', {
        'gatepass': gatepass,
        'error': error,
    })

def find_outpass(request):
    gatepass = None  # Initialize variable to hold the found gatepass
    error = None  # Variable to hold any error messages

    if request.method == 'POST':
        gatepass_no = request.POST.get('gatepassno')

        # Try to fetch the Gatepass from the database
        try:
            outpass = Outpass.objects.get(gatepassno=gatepass_no)
        except Gatepass.DoesNotExist:
            error = 'Gatepass not found. Please check the Gatepass number and try again.'

    return render(request, 'find_outpass.html', {
        'outpass': outpass,
        'error': error,
    })

def edit_out_pass(request, gatepassno):



    try:
        gatepass = Gatepass.objects.get(gatepassno=gatepassno)
    except DoesNotExist:
        return render(request, '404.html')  # Handle not found

    if request.method == 'POST':
        new_gatepassno = request.POST.get('gatepassno')
        new_token = request.POST.get('token')

        #Check if the new gatepassno already exists in a different record
        existing_gatepass = Gatepass.objects(gatepassno=new_gatepassno).first()
        if existing_gatepass and new_gatepassno != gatepass.gatepassno:
            errors = {'gatepassno': 'Gate Pass No. already exists.'}
            return render(request, 'edit_out_pass.html', {'gatepass': gatepass, 'errors': errors})

        #Check if the new token already exists in a different record
        # existing_token = Gatepass.objects(token=new_token).first()
        # if existing_token and new_token != gatepass.token:
        #     errors = {'token': 'Token already exists.'}
        #     return render(request, 'edit_out_pass.html', {'gatepass': gatepass, 'errors': errors})

        # Update fields
        gatepass.gatepassno = new_gatepassno
        gatepass.driver_name = request.POST.get('driver_name')
        gatepass.purpose = request.POST.get('purpose')
        gatepass.vehicle_number = request.POST.get('vehicle_number')
        gatepass.owner_contact_no = request.POST.get('owner_contact_no')
        gatepass.Access_Area = request.POST.get('Access_Area')
        gatepass.token = new_token
        gatepass.Restricted_Area = request.POST.get('Restricted_Area')

        # Save the updated Gatepass
        gatepass.save()
        return redirect('edit_pass_success', gatepassno=gatepass.gatepassno)

    return render(request, 'edit_out_pass.html', {'gatepass': gatepass})

def edit_pass_success(request,gatepassno):
    
    return render(request,'edit_pass_success.html',{'gatepass':gatepassno}) 







def save_out_pass(request):
    if request.method == 'POST':
        # Retrieve data from the request
        gatepassno = request.POST.get('gatepassno')
        token = request.POST.get('token')
        vehicle_number = request.POST.get('vehicle_number')
        driver_name = request.POST.get('driver_name')
        owner_contact_no = request.POST.get('owner_contact_no')
        purpose = request.POST.get('purpose')
        Access_Area = request.POST.get('Access_Area')
        Restricted_Area = request.POST.get('Restricted_Area')

        # Create and save the Outpass document
        out_pass = Outpass(
            gatepassno=gatepassno,
            token=token,
            vehicle_number=vehicle_number,
            driver_name=driver_name,
            owner_contact_no=owner_contact_no,
            purpose=purpose,
            Access_Area=Access_Area,
            Restricted_Area=Restricted_Area
        )
        out_pass.save()  # Save the document to the database

        return JsonResponse({'message': 'Out pass saved successfully!'}, status=201)
    return render(request, 'out_pass_success.html')
    # return JsonResponse({'error': 'Invalid request method.'}, status=405)