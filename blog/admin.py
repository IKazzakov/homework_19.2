from django.contrib import admin

from blog.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'views_count',)
    list_filter = ('is_published', 'views_count',)
    search_fields = ('title', 'content',)
    prepopulated_fields = {'slug': ('title',)}
