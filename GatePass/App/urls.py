from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    # path('registersuccess/',views.registersuccess,name='registersuccess'),
    path('home/',views.home,name='home'),
    path('form/', views.form,name='form'),
    path('logout/',views.logout_view,name='logout'),
    # path('submit/form/',views.submit_form,name='submit_form'),
    path('receipt/<gatepass_id>/', views.receipt, name='receipt'),  #<gatepass_id>
    path('edit-gatepass/<str:gatepass_id>/', views.edit_gatepass_view, name='edit_gatepass_view'),
    # path('get-gate-pass-data/',views.delete_form, name='get_gate_pass_data'),
    
    # path('submitform/',views.submit_form,name='Submit form'),
    
    
]