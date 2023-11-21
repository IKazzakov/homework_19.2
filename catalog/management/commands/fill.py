from django.core.management import BaseCommand
from config.settings import BASE_DIR
from catalog.models import Category, Product
# from django.shortcuts import get_object_or_404
import os
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        path_to_categories = os.path.join(BASE_DIR, 'catalog/fixtures/categories.json')
        path_to_products = os.path.join(BASE_DIR, 'catalog/fixtures/products.json')

        Category.objects.all().delete()
        Product.objects.all().delete()

        with open(path_to_categories) as f:
            categories = json.load(f)
            categories_for_create = []
            for category in categories:
                categories_for_create.append(Category(**category['fields']))

            Category.objects.bulk_create(categories_for_create)

        with open(path_to_products) as f:
            products = json.load(f)
            products_for_create = []
            for product in products:
                category_id = product['fields']['category']
                product['fields']['category'] = Category.objects.get(pk=category_id)
                products_for_create.append(Product(**product['fields']))

            Product.objects.bulk_create(products_for_create)

