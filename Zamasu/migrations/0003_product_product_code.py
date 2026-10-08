import random

from django.db import migrations, models


def generate_product_code():
    return str(random.randint(10000000, 99999999))


def populate_product_codes(apps, schema_editor):
    Product = apps.get_model('Zamasu', 'Product')
    used_codes = set(Product.objects.exclude(product_code='').exclude(product_code__isnull=True).values_list('product_code', flat=True))

    for product in Product.objects.order_by('product_id'):
        if product.product_code and product.product_code not in used_codes:
            used_codes.add(product.product_code)
            continue

        while True:
            code = generate_product_code()
            if code not in used_codes:
                used_codes.add(code)
                product.product_code = code
                product.save(update_fields=['product_code'])
                break


class Migration(migrations.Migration):

    dependencies = [
        ('Zamasu', '0002_alter_product_price_alter_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, default='', editable=False, max_length=8, null=True),
        ),
        migrations.RunPython(populate_product_codes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default=generate_product_code, editable=False, max_length=8, unique=True),
        ),
    ]
