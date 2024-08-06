from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import ShoeAttribute
from .cart import CartMananger
from django.contrib.auth.decorators import login_required
# from orders.models import Order
import uuid

@require_POST
def add_to_cart(request, shoe_attribute_id):
    """add an item to cart"""
    cart = CartMananger(request)
    shoe_attribute = get_object_or_404(ShoeAttribute, id=shoe_attribute_id)
    cart.add(shoe_attribute=shoe_attribute, quantity=1)
    return redirect("cart:cart-detail-view")

@require_POST
def remove_from_cart(request, shoe_attribute_id):
    """remove an item from the cart"""
    cart = CartMananger(request)
    shoe_attribute = get_object_or_404(ShoeAttribute, id=shoe_attribute_id)
    cart.remove(shoe_attribute)
    return redirect("cart:cart-detail-view")
@login_required(login_url="login-view")
def cart_detail(request):
    """Display the contents of the cart"""
    cart = CartMananger(request)
    return render(request, "cart/cart-detail2.html", {"cart": cart})

@login_required(login_url="login-view")
def checkout_view(request, shoe_attribute_id):
    # Get the current user's email and name
    email = request.user.email
    name = request.user.get_full_name()
    
    # Generate a unique transaction reference (you can use UUID or any other method)
    tx_ref = str(uuid.uuid4())
    
    # Calculate the total amount
    cart = CartMananger(request)
    amount = cart.get_total_price()
    
    # Prepare the redirect URL (e.g., to a success or order confirmation page)
    redirect_url = 'https://yourdomain.com/payment-success/'
    
    # Currency (e.g., USD)
    currency = 'USD'
    
    context = {
        'email': email,
        'name': name,
        'tx_ref': tx_ref,
        'amount': amount,
        'redirect_url': redirect_url,
        'currency': currency,
    }
    
    return render(request, 'cart/checkout.html', context)
