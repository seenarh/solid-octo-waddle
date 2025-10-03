from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.decorators import method_decorator
from .models import Post,Comment

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'all_posts_list'

@login_required
def post_new(request):
    # allow only staff & superusers
    if not request.user.is_staff:
        return redirect('main')  

    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")

        if title and body:
            post = Post.objects.create(
                title=title,
                text=body,
            )
            post.save()
            return redirect('main')

    return render(request, 'post_new.html')

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


    

