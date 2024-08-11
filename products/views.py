from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Shoe,
        ShoeAttribute,
            ShoeImage,
)
from django.contrib.auth.decorators import login_required

from .forms import (
    ShoeForm, ShoeAttributeForm, ShoeImageForm
)



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


@login_required(login_url="login-view")
def add_shoe_view(request):
    if request.method == "POST":
        shoe_form = ShoeForm(request.POST)
        attribute_form = ShoeAttributeForm(request.POST)
        image_form = ShoeImageForm(request.POST, files=request.FILES)

        if shoe_form.is_valid() and attribute_form.is_valid() and image_form.is_valid():
            shoe = shoe_form.save()
            shoe_attribute = attribute_form.save(commit=False)
            shoe_attribute.shoe = shoe
            shoe_attribute.save()
            
            attribute_form.save_m2m()
            shoe_image = image_form.save(commit=False)
            shoe_image.shoe_attribute = shoe_attribute
            shoe_image.save()

            return redirect("products:shoe-list")
        else:
            print("Shoe Form Errors: ", shoe_form.errors)
            print("Attribute Form Errors: ", attribute_form.errors)
            print("Image Form Errors: ", image_form.errors)
    else:
        shoe_form = ShoeForm()
        attribute_form = ShoeAttributeForm()
        image_form = ShoeImageForm()


    context = {
        "shoe_form": shoe_form,
        "attribute_form": attribute_form,
        "image_form": image_form
    }
    return render(request, 'products/add-shoe.html', context)
