from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blog.models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Posts',
    }


class PostCreateView(CreateView):
    model = Post
    extra_context = {
        'title': 'Create post',
    }
    fields = ['title', 'slug', 'content', 'image', 'is_published']
    success_url = reverse_lazy('blog:post_list')
