from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cart', 'city', 'phone', 'status', 'address', 'payment_method', 'is_paid', 'postal_code']
