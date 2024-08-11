from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogTag, Comment


admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(BlogTag)
admin.site.register(Comment)

