from django.urls import path
from .views import (
    shoe_list_view,
      shoe_detail_view,
        shoe_3d_view)


app_name = "products"



urlpatterns = [
    path('shoe/', shoe_list_view, name='shoe-list'),
    path('shoe/<slug:slug>/', shoe_detail_view, name='shoe-detail'),
    path('shoe/<slug:slug>/3d/', shoe_3d_view, name='shoe-3d-view'),
]
