from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'quantity', 'price', 'supplier')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Ballpen'}),
            'category': forms.TextInput(attrs={'placeholder': 'e.g. School Supplies'}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'supplier': forms.TextInput(attrs={'placeholder': 'e.g. ABC Trading'}),
        }
        