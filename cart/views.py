from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import ShoeAttribute
from .cart import CartMananger
from django.contrib.auth.decorators import login_required
from orders.models import Order
import uuid
from django.conf import settings
import requests
from django.http import JsonResponse

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
def checkout_view(request):
    # Get the current user's email and name
    email = request.user.email
    name = request.user.get_full_name()
    
    # Generate a unique transaction reference (you can use UUID or any other method)
    tx_ref = str(uuid.uuid4())
    
    # Calculate the total amount
    cart = CartMananger(request)
    amount = cart.get_total_price()
    
    # Prepare the redirect URL (e.g., to a success or order confirmation page)
    redirect_url = ' https://6e0d-105-161-4-104.ngrok-free.app'
    
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

def payment_success_view(request):
    # Get the parameters from the URL
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    if status == 'successful':
        # Assume you have an Order model with a `tx_ref` field
        try:
            order = get_object_or_404(Order, tx_ref=tx_ref)
            
            # Flutterwave verification API call
            url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
            headers = {
                "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            }
            response = requests.get(url, headers=headers)
            result = response.json()

            if result['status'] == 'success' and result['data']['amount'] == order.amount and result['data']['currency'] == order.currency:
                # Update order status
                order.status = 'Paid'
                order.save()

                # Render the payment success template
                return render(request, 'payment-success.html', {
                    'user': request.user,
                    'tx_ref': tx_ref,
                    'amount': order.amount,
                    'currency': order.currency,
                })

            else:
                return JsonResponse({'success': False, 'message': 'Payment verification failed'})
        
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})

    # Handle the case where payment was not successful
    return JsonResponse({'success': False, 'message': 'Payment was not successful'})
