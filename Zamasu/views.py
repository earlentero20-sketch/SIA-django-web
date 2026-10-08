from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import ProductForm
from .models import Product


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created. Please log in.')
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def index(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all().order_by('-date_added')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(supplier__icontains=query) |
            Q(product_code__icontains=query)
        )

    return render(request, 'Zamasu/product_list.html', {'products': products, 'query': query})


@login_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.status = 'Available' if product.quantity > 0 else 'Out_of_stock'
        product.save()
        messages.success(request, 'Product added to inventory.')
        return redirect('product-list')
    return render(request, 'Zamasu/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.status = 'Available' if product.quantity > 0 else 'Out_of_stock'
        product.save()
        messages.success(request, 'Product updated.')
        return redirect('product-list')
    return render(request, 'Zamasu/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product removed from inventory.')
        return redirect('product-list')
    return render(request, 'Zamasu/product_confirm_delete.html', {'product': product})