from django.urls import path
from blog.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView
from blog.apps import BlogConfig

app_name = BlogConfig.name
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('view/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]
