from django.urls import path 
from .views import (
    register_view,
      home_view,
        login_view,
          logout_view,
            password_reset_view,
              profile_update_view,
              ) 


app_name = 'accounts'

urlpatterns = [
    path('home', home_view, name='home'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('profile-update', profile_update_view, name='profile_update'),
    path('forgot-password', password_reset_view, name='forgot_password'),
    path('logout', logout_view, name='logout'),
    

]
