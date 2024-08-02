from django.urls import path 
from .views import *

from . import views


urlpatterns = [
    path('', home_view, name='home-view'),
    path('login', login_view, name='login-view'),
    path('register', register_view, name='register-view'),
    path('profile-update', profile_update_view, name='profile-update'),
    path('forgot-password', password_reset_view, name='forgot-password'),
    path('logout', logout_view, name='logout-view'),
    path('profile-password-change', profile_password_change, name='profile-password-change'),
    path('reset_password/<str:uid>/<str:token>/', reset_password, name='reset_password'),
    

    path('user-profile', views.user_profile, name='user-profile'),
    

]
