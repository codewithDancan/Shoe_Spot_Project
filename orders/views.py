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


@login_required(login_url="login-view")
def order_create(request):
    form = OrderForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect("orders:order-list")
    context = {
        "form": form,
    }
    return render(request, "orders/order-form.html", context)
        
        
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

