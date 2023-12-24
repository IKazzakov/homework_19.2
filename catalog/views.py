from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from catalog.forms import ProductForm
from catalog.models import Product, Version


# Create your views here.
class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница',
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        for product in context_data['object_list']:
            active_version = Version.objects.filter(product=product, is_active_version=True).last()
            if active_version:
                product.active_version_number = active_version.version_number
                product.active_version_name = active_version.name
            else:
                product.active_version_number = None
                product.active_version_name = None
        return context_data


class ProductCreateView(CreateView):
    model = Product
    extra_context = {
        'title': 'Create product',
    }
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Товар',
    }


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}, phone: {phone}, message: {message}')
        return render(request, 'catalog/contacts.html', self.extra_context)
