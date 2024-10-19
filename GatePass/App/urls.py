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
    path('logout/',views.logout_view,name='logout')
    
    
    
]