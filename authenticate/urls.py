from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ="home"),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('process_data/', views.process_data, name='process_data'),
    path('clear_history/', views.clear_history, name='clear_history'),
    path('index/', views.IndexPage, name='Index'),
]

