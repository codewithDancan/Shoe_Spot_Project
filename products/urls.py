from django.urls import path
from .views import *


app_name = "products"



urlpatterns = [
    path('shoe/', shoe_list_view, name='shoe-list'),
    path('add/shoe/', add_shoe_view, name='add-shoe'),
    path('shoe/<slug:slug>/', shoe_detail_view, name='shoe-detail'),
    path('shoe/<slug:slug>/3d/', shoe_3d_view, name='shoe-3d-view'),
]
