from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Post,Comment
from .forms import PostForm
from django.urls import reverse_lazy


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'all_posts_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [{'slug': slug, 'name': name} for slug, name in Post.CATEGORY_CHOICES]
        context['current_category'] = None
        return context
    
class CategoryListView(ListView):
    model = Post
    template_name ='category_detail.html'
    context_object_name = 'all_posts_list'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Post.objects.filter(category=category_slug).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = [{'slug': slug, 'name': name} for slug, name in Post.CATEGORY_CHOICES]
        context['categories'] = categories
        category_slug = self.kwargs['category_slug']
        context['current_category'] = next((c for c in categories if c['slug'] == category_slug), None)
        return context

@login_required
def post_new(request):
    # Only staff/superusers can post
    if not request.user.is_staff:
        return redirect('main')

    # Capture category slug from query string (?category=tech)
    category_slug = request.GET.get("category")

    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        category = request.POST.get("category") or category_slug

        if title and body and category:
            post = Post.objects.create(
                title=title,
                text=body,
                category=category,
                author=request.user
            )
            return redirect('post_detail', pk=post.pk)

    # Pass category choices and selected category to template
    return render(request, "post_new.html", {
        "category_slug": category_slug,
        "categories": Post.CATEGORY_CHOICES,
    })


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    '''def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.all().order_by("-created_at")
        return context'''
    
    def get(self, request, *args , **kwargs):
        post = self.get_object()
        comments = post.comments.all().order_by("-created_at")
        return render(request, "post_detail.html", {"post": post, "comments": comments})

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        body = request.POST.get("body")
        if body and request.user.is_authenticated:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=body,
            )
        return redirect("post_detail", pk=post.pk)

# Edit Post
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'  # you’ll create this file next
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


# Delete Post
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'  # you’ll create this file next
    success_url = reverse_lazy('main')