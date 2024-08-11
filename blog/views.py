from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, BlogCategory, BlogTag, Comment
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import (
    BlogPostForm
)

def blog_list_view(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/blog-list.html", {"page_obj": page_obj})

def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.all()
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        content = request.POST["content"]
        Comment.objects.create(post=post, name=name, email=email, content=content)
        return HttpResponseRedirect(reverse("blog:blog-detail", args=[slug]))
    return render(request, "blog/blog-detail.html", {"post": post, "comments": comments})

def blog_category_view(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(category=category)
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/blog-category.html", {"category": category, "page_obj": page_obj})

def blog_tag_view(request, slug):
    tag = get_object_or_404(BlogTag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag)
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/blog-tag.html", {"tag": tag, "page_obj": page_obj})

def add_blog_post_view(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Set the author as the logged-in user
            blog_post.save()
            form.save_m2m()  # Save the many-to-many data for tags
            return redirect("blog-list-view")  # Redirect to the blog list view after successful post creation
    else:
        form = BlogPostForm()
   

  
    return render(request, "blog/add-blog-post.html", {"form": form})

