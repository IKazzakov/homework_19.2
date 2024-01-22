from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version, Category
from catalog.services import get_cached_categories


# Create your views here.
class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.seller != self.request.user:
            raise PermissionError('Недостаточно прав для просмотра данного продукта')
        return self.object

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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    extra_context = {
        'title': 'Create product',
    }
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.seller = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Товар',
    }


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    permission_required = 'catalog.change_product'
    extra_context = {
        'title': 'Update product',
    }
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.seller = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)

    def test_func(self):
        return self.get_object().seller == self.request.user

    def handle_no_permission(self):
        raise PermissionError('Недостаточно прав для редактирования данного продукта')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        return self.get_object().seller == self.request.user

    def handle_no_permission(self):
        raise PermissionError('Недостаточно прав для удаления данного продукта')


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


class CategoriesListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории',
    }
    template_name = 'catalog/categories.html'

    def get_queryset(self):
        return get_cached_categories()
