from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
import uuid

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ShoeColor(AbstractBaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False, unique=True, blank=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Shoe Colors"

class ShoeSize(AbstractBaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False, unique=True, blank=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Shoe Sizes"

class ShoeCategory(AbstractBaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False, unique=True, blank=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Shoe Categories"

class Shoe(AbstractBaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ShoeCategory, on_delete=models.CASCADE, related_name="shoes")
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ShoeAttribute(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.ManyToManyField(ShoeSize, blank=True, related_name="sizes")
    color = models.ForeignKey(ShoeColor, on_delete=models.CASCADE, null=True, blank=True, related_name="color")
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name="attributes")
    stock = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["shoe", "color"], name="unique_shoe_attribute")]

    def __str__(self):
        return f"{self.shoe.name} - {self.color.name if self.size else 'N/A'} - {self.size.name if self.size else 'N/A'}"
    
class ShoeImage(AbstractBaseModel):
    class AngleChoices(models.TextChoices):
        FRONT = "front", "Front"
        BACK = "back", "Back"
        DETAIL = "detail", "Deatil"
        UNSPECIFIED = "unspecified", "Unspecified"

    shoe_attribute = models.ForeignKey(ShoeAttribute, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="shoe_images/")
    is_primary = models.BooleanField(default=False)
    angle = models.CharField(max_length =50, choices=AngleChoices.choices, default=AngleChoices.UNSPECIFIED)

    class Meta:
        ordering = ["angle"]

    def __str__(self):
        return f"Image for {self.shoe_attribute.color} - {self.get_angle_display()}"
    

    

    


