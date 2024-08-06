from django.shortcuts import render, get_object_or_404
from .models import (
    Shoe,
        ShoeAttribute,
            ShoeImage,
)
from django.contrib.auth.decorators import login_required
@login_required(login_url="login-view")
def shoe_list_view(request):
    shoes = Shoe.objects.all()
    context = {
        'shoes': shoes,
    }
    return render(request, 'products/shoe-list.html', context)
@login_required(login_url="login-view")
def shoe_detail_view(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    shoe_attributes = ShoeAttribute.objects.filter(shoe=shoe)
    primary_image = ShoeImage.objects.filter(shoe_attribute__shoe=shoe, is_primary=True).first()
    context = {
        'shoe': shoe,
        'shoe_attributes': shoe_attributes,
        'primary_image': primary_image,
    }
    return render(request, 'products/shoe-detail.html', context)
@login_required(login_url="login-view")
def shoe_3d_view(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    shoe_images = ShoeImage.objects.filter(shoe_attribute__shoe=shoe)
    return render(request, 'products/shoe-3d.html', {
        'shoe': shoe,
        'shoe_images': shoe_images,
    })


