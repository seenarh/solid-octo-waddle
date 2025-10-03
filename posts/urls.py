from django.urls import path
from .views import PostListView,post_new,PostDetailView

urlpatterns = [
        path('main/', PostListView.as_view(), name='main'),
        path('post_new/', post_new, name='post_new'),    
        path('main/<int:pk>',PostDetailView.as_view(), name='post_detail')    

]