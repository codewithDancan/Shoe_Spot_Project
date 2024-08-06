from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('order/', views.order_list, name='order-list'),
    path('order/<uuid:order_id>/', views.order_detail, name='order-detail'),
    path('order/new/', views.order_create, name='order-create'),
    path('order/<uuid:order_id>/edit/', views.order_update, name='order-update'),
    path('order/<uuid:order_id>/delete/', views.order_delete, name='order-delete'),
]
