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
    # path('form/<int:token>/',views.edit_form,name='edit form'),
    path('logout/',views.logout_view,name='logout'),
    # path('submit/form/',views.submit_form,name='submit_form'),
    path('receipt/<gatepass_id>/', views.receipt, name='receipt'),  #<gatepass_id>
    # path('edit-gatepass/<str:gatepass_id>/', views.edit_gatepass_view, name='edit_gatepass_view'),
    # path('get-gate-pass-data/',views.delete_form, name='get_gate_pass_data'),
    path('request_out_pass/', views.request_out_pass, name='request_out_pass'),
    path('fetch_out_pass/', views.fetch_out_pass, name='fetch_out_pass'),
    path('out_pass_success/<int:gatepassno>/', views.out_pass_success, name='out_pass_success'),
    path('save_out_pass/', views.save_out_pass, name='save_out_pass'),
    path('outpass/<int:gatepassno>/', views.display_outpass, name='display_outpass'),
    path('edit_out_pass/<int:gatepassno>/', views.edit_out_pass, name='edit_out_pass'),
    # path('edit_outpass/<int:gatepassno>/',views.edit_out_pass,name="edit_outpass"),
    path('edit_pass_success/<int:gatepassno>/',views.edit_pass_success,name='edit_pass_success'),
    path('gatepass/update/<int:gatepassno>/', views.update_gatepass, name='update_gatepass'),

    path('update_success/<int:gatepassno>/',views.update_success_page,name='update_success_page'),
    path('outpass/update/<int:gatepassno>/',views.update_outpass,name='update_outpass'),
    path('update_outpass_success/<int:gatepassno>/',views.update_outpass_success_page,name='update_outpass_success_page'),
    path('gatepass/delete/', views.delete_gatepass, name='delete_gatepass'),
    path('outpass/delete/',views.delete_outpass,name='delete_outpass'),
    path('find_gatepass/', views.find_gatepass, name='find_gatepass'),
    path('find_outpass/',views.find_outpass,name='find_outpass'),

    # path('submitform/',views.submit_form,name='Submit form'),
    
    
]