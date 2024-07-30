from django.db import models
from products.models import (
    AbstractBaseModel,
)
from django.utils.translation import gettext_lazy as _
import uuid
from cart.models import Cart
from .validators import ValidationError, validate_unique_city_name, validate_unique_country_name
import random
import string

def generate_unique_reference_number():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=7))

class Country(AbstractBaseModel):
    name = models.CharField(max_length=100, validators=[validate_unique_country_name])

    def __str__(self):
        return f"{self.name}"


class City(AbstractBaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country}"
    
    """class Meta:
        constraints = models.UniqueConstraint(fields=["name", "country"], name="unique_city_name_country_case_insensitive")"""

    def clean(self):
        validate_unique_city_name(self.name, self.country)
        if not hasattr(self, "country"):
            raise ValidationError("City must have a country.")

class Order(AbstractBaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending", _("Pending")
        PROCESSING = "Procesing", _("Processing")
        SHIPPED = "Shipped", _("Shipped")
        DELIVERED = "Delivered", _("Delivered")
        CANCELED = "Canceled", _("Canceled")

    class PaymentMethods(models.TextChoices):
        PAYPAL = "Paypal", _("Paypal")
        CARD = "Card", _("Card")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    phone = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    address = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    payment_method = models.CharField(max_length=50, choices=PaymentMethods.choices, default=PaymentMethods.PAYPAL)
    is_paid = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Order: {self.reference_number}"
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = generate_unique_reference_number()
            # ensure unique reference number 
            while Order.objects.filter(reference_number=self.reference_number).exists():
                self.reference_number = generate_unique_reference_number()
        super().save(*args, **kwargs)