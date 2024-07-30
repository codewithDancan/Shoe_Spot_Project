from django.db import models
from django.contrib.sessions.models import Session
from products.models import (
    AbstractBaseModel,
    ShoeAttribute)
import uuid


class Cart(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name="cart")
    is_checked_out = models.BooleanField(default=False)


    def __str__(self):
        return f" Cart for session {self.session.session_key}"
    
class CartItem(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    shoe_attribute = models.ForeignKey(ShoeAttribute, on_delete=models.CASCADE)

    @property
    def get_cart_item_total_price(self):
        return self.shoe_attribute.shoe.price * self.quantity
    
    class Meta:
        ordering = ["-created_at"]




    

    

