# blog/urls.py
from django.urls import path
from .views import (
    blog_category_view,
      blog_detail_view,
        blog_list_view, 
        blog_tag_view, 
        add_blog_post_view
)

app_name = "blog"

urlpatterns = [

    path('blog/', blog_list_view, name='blog-list'),
    path('blog/category/<slug:slug>/', blog_category_view, name='blog-category'),
    path('blog/tag/<slug:slug>/', blog_tag_view, name='blog-tag'),
    path('blog/add/', add_blog_post_view, name='add-blog'),
    path('blog/<slug:slug>/', blog_detail_view, name='blog-detail'),
]
