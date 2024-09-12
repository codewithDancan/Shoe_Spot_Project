from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import ShoeAttribute
from .cart import CartMananger
from django.contrib.auth.decorators import login_required
from orders.models import Order, City
import uuid, json
from django.conf import settings
import requests
from django.http import JsonResponse
from .models import CartItem, Cart
from orders.validators import ValidationError
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt
from orders.forms import OrderForm



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
    try:
        cart = Cart.objects.get(session=request.session.session_key)
    except Cart.DoesNotExist:
        return redirect('cart:cart-detail-view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        print("POST Data:", request.POST) 
        if form.is_valid():
            order = form.save(commit=False)
            order.cart = cart
            order.save()
            
            # Fetchs the order details
            city = order.city
            phone = order.phone
            address = order.address
            postal_code = order.postal_code
            
            context = {
                'email': request.user.email,
                'name': request.user.get_full_name(),
                'tx_ref': str(uuid.uuid4()),
                'amount': CartMananger(request).get_total_price(),
                'redirect_url': 'https://6e0d-105-161-4-104.ngrok-free.app',
                'currency': 'USD',
                'quantity': cart.__len__(),
                'form': form,
                'cart': cart,
                'city': city,
                'phone': phone,
                'address': address,
                'postal_code': postal_code,
            }

            return render(request, 'cart/checkout.html', context)
        else:
            print("Form Errors:", form.errors) 
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = OrderForm()

    context = {
        'email': request.user.email,
        'name': request.user.get_full_name(),
        'tx_ref': str(uuid.uuid4()),
        'amount': CartMananger(request).get_total_price(),
        'redirect_url': 'https://6e0d-105-161-4-104.ngrok-free.app',
        'currency': 'USD',
        'quantity': CartMananger(request).__len__(),
        'form': form,
        'cart': cart,
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



@csrf_exempt
def paypal_payment_success_view(request, order_id):
    try:
        # Fetch the order using the order ID
        order = get_object_or_404(Order, reference_number=order_id)

        # Update the order status to indicate payment is successful
        order.is_paid = True
        order.status = Order.OrderStatus.PROCESSING
        order.save()

        # Clear the cart after successful payment
        cart_manager = CartMananger(request)
        cart_manager.clear()

        return render(request, 'payment_success.html', {'order': order})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def paypal_payment_failed_view(request):
    """Handles failed payment."""
    return render(request, 'payment-failed.html', {
        'message': 'Payment was not successful. Please try again.'
    })
