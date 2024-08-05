from django.urls import path
from .views import (
    add_to_cart,
    remove_from_cart,
    cart_detail,
    checkout_view,
)

app_name = "cart"

urlpatterns = [
    path("cart/", cart_detail, name="cart-detail-view"),
    path("cart/add/<uuid:shoe_attribute_id>/", add_to_cart, name="add-to-cart-view"),
    path("cart/remove/<uuid:shoe_attribute_id>/", remove_from_cart, name='remove-from-cart-view'),
    path("checkout/<uuid:shoe_attribute_id>/", checkout_view, name="checkout-view")
]
