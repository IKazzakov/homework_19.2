from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, \
    ProductUpdateView, CategoriesListView

app_name = CatalogConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_update'),
    path('delete/<int:pk>/', never_cache(ProductDeleteView.as_view()), name='product_delete'),
]
