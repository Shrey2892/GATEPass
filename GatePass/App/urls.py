from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    # path('registersuccess/',views.registersuccess,name='registersuccess'),
    path('home/',views.home,name='home'),
    path('form/', views.get_form,name='form'),
    path('logout/',views.logout_view,name='logout'),
    path('form/submit/',views.submit_form,name='submit_form'),
    path('receipt/<gatepass_id>/', views.receipt_view, name='receipt'),
    
    # path('submitform/',views.submit_form,name='Submit form'),
    
    
]