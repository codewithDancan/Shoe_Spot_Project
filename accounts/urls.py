from django.urls import path 
from .views import (
    register_view,
      home_view,
        login_view,
          logout_view,
            password_reset_view,
              profile_update_view,
              )

from . import views


urlpatterns = [
    path('', home_view, name='home-view'),
    path('login', login_view, name='login-view'),
    path('register', register_view, name='register-view'),
    path('profile-update', profile_update_view, name='profile-update'),
    path('forgot-password/<int:id>', password_reset_view, name='forgot-password'),
    path('logout', logout_view, name='logout-view'),

    path('single', views.single, name='single'),
    

]
