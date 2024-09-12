from django.urls import path
from .views import (
    add_to_cart,
    remove_from_cart,
    cart_detail,
    checkout_view,
    payment_success_view,
    paypal_payment_failed_view,
    paypal_payment_success_view
)

app_name = "cart"

urlpatterns = [
    path("cart/", cart_detail, name="cart-detail-view"),
    path("cart/add/<uuid:shoe_attribute_id>/", add_to_cart, name="add-to-cart-view"),
    path("cart/remove/<uuid:shoe_attribute_id>/", remove_from_cart, name='remove-from-cart-view'),
    path("checkout/", checkout_view, name="checkout-view"),
    path("paypal-payment-success/", paypal_payment_success_view, name="paypal-payment-success"),
    path("paypal-payment-failed/", paypal_payment_failed_view, name="paypal-payment-failed"),
    path("payment-success/", payment_success_view, name="payment-success"),
]
