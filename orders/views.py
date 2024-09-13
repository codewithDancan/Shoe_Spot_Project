from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, City
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import paypalrestsdk
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from cart.cart import CartMananger
from django.views.decorators.http import require_POST, require_GET
import json
from django.urls import reverse
from cart.models import Cart

paypalrestsdk.configure({
  "mode": settings.PAYPAL_MODE,
  "client_id": settings.PAYPAL_CLIENT_ID,
  "client_secret": settings.PAYPAL_CLIENT_SECRET,
})



@login_required(login_url="login-view")
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order-list.html', {'orders': orders})
@login_required(login_url="login-view")
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order-detail.html', {'order': order})

@require_POST
@login_required(login_url="login-view")
def order_create(request):
    print(request.POST)
    # Handle form-encoded data instead of JSON
    cart = request.POST.get('cart')
    city_id = request.POST.get('city')
    phone = request.POST.get('phone')
    status = request.POST.get('status')
    address = request.POST.get('address')
    payment_method = request.POST.get('payment_method')

    # Validate required fields
    if not all([cart, city_id, phone, address, status, payment_method]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Retrieve the cart associated with the current session
    try:
        cart = Cart.objects.get(session=request.session.session_key)
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart does not exist'}, status=400)

    # Fetch the city
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return JsonResponse({'error': 'City does not exist'}, status=400)

    # Create the order
    order = Order(
        cart=cart,
        city=city,
        phone=phone,
        address=address,
        payment_method=Order.PaymentMethods.PAYPAL,
        status=Order.OrderStatus.PENDING,
        is_paid=False
    )
    order.save()

    # Create the PayPal payment
    cart_manager = CartMananger(request)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(cart_manager.get_total_price()),
                "currency": "USD"
            },
            "description": f"Order {order.reference_number}"
        }],
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('orders:capture-order', args=[order.id])),
            "cancel_url": request.build_absolute_uri(reverse('cart:cart-detail-view'))
        }
    })

    # Attempt to create the PayPal payment
    if payment.create():
        order.payment_id = payment.id
        order.save()
        return JsonResponse({'orderID': payment.id})
    else:
        return JsonResponse({'error': payment.error}, status=500)

    

@login_required(login_url="login-view")
def capture_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    payment_id = order.payment_id

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": request.POST.get('payerID')}):
        order.is_paid = True
        order.status = Order.OrderStatus.PROCESSING
        order.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': payment.error}, status=500)
        
        
@login_required(login_url="login-view")
def order_update(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders:order-list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order-form.html', {'form': form})
@login_required(login_url="login-view")
def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('orders:order-list')
    return render(request, 'orders/order-confirm-delete.html', {'order': order})

