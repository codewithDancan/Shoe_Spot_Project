from django import forms
from .models import Shoe, ShoeAttribute, ShoeImage


class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = "__all__"

class ShoeAttributeForm(forms.ModelForm):
    class Meta:
        model = ShoeAttribute
        fields = "__all__"

class ShoeImageForm(forms.ModelForm):
    class Meta:
        model = ShoeImage
        fields = "__all__"