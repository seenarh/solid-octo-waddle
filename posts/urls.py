from django.urls import path
from .views import PostListView,post_new,PostDetailView,PostUpdateView,PostDeleteView,CategoryListView
from . import views

urlpatterns = [
        path('main/', PostListView.as_view(), name='main'),
        path('post_new/', post_new, name='post_new'),    
        path('main/<int:pk>',PostDetailView.as_view(), name='post_detail'), 
        path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
        path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
        path('category/<str:category_slug>/', CategoryListView.as_view(), name='category_posts'),
]
