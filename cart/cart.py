from decimal import Decimal
from django.conf import settings
from products.models import ShoeAttribute
from .models import Cart, CartItem
from django.contrib.sessions.models import Session

class CartMananger:
    def __init__(self, request):
        """initializing the cart"""
        self.session = request.session
        session_key = self.session.session_key
        if not session_key:
            self.session.save()
            session_key = self.session.session_key
        
        try:
            self.cart = Cart.objects.get(session__session_key=session_key)
        except Cart.DoesNotExist:
            session_instance = Session.objects.get(session_key=session_key)
            self.cart = Cart(session=session_instance)
            self.cart.save()

        
    def add(self, shoe_attribute, quantity=1, override_quantity=False):
        """Add a shoe to the cart or update its quantity"""
        cart_item, created = CartItem.objects.get_or_create(cart=self.cart, shoe_attribute=shoe_attribute)
        if created or override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

    def remove(self, shoe_attribute):
        """remove a shoe from the cart"""
        try:
            cart_item = CartItem.objects.get(cart=self.cart, shoe_attribute=shoe_attribute)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    def __len__(self):
        """Count all shoes/items in the cart"""
        return sum(item.quantity for item in CartItem.objects.filter(cart=self.cart))
    
    def get_total_price(self):
        """Calculate the total price of all shoes/items in the cart"""
        return sum(item.get_cart_item_total_price for item in CartItem.objects.filter(cart=self.cart))
    
    def __iter__(self):
        for item in CartItem.objects.filter(cart=self.cart):
            yield item
    
    def clear(self):
        """Clear the cart by deleting all CartItems and removing the Cart ID from the session"""
        CartItem.objects.filter(cart=self.cart).delete()
        self.session[settings.CART_SESSION_ID] = None
