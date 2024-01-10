from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Posts',
    }

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    extra_context = {
        'title': 'Create post',
    }
    fields = ['title', 'content', 'image', 'is_published']
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    extra_context = {
        'title': 'Update post',
    }
    fields = ['title', 'content', 'image', 'is_published']

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs.get('slug')])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
