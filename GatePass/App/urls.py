from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    # path('registersuccess/',views.registersuccess,name='registersuccess'),
    path('home/',views.home,name='home'),
    
]