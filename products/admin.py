from django.contrib import admin
from .models import (
    Shoe,
        ShoeAttribute,
            ShoeCategory,
                ShoeColor,
                    ShoeSize,
                        ShoeImage
)

admin.site.register(Shoe)
admin.site.register(ShoeAttribute)
admin.site.register(ShoeCategory)
admin.site.register(ShoeColor)
admin.site.register(ShoeSize)
admin.site.register(ShoeImage)

