from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('product_id', 'name', 'category', 'quantity', 'price', 'supplier', 'status', 'date_added')
	list_filter = ('category', 'status')
	search_fields = ('name', 'supplier')
