from django.urls import path
from .views import (
    order_list,
    order_detail,
    order_create, 
    order_delete,
    order_update,
    capture_order,
)

app_name = "orders"


urlpatterns = [
    path('order/', order_list, name='order-list'),
    path('order/<uuid:order_id>/', order_detail, name='order-detail'),
    path('new-order/', order_create, name='order-create'),
    path('capture-order/<uuid:order_id>/', capture_order, name='capture-order'),
    path('order/<uuid:order_id>/edit/', order_update, name='order-update'),
    path('order/<uuid:order_id>/delete/', order_delete, name='order-delete'),
]
