from django.urls import path
from  . import views
from .views import (
    PostListView, PostDetailView, 
    PostCreateView, PostUpdateView,
    PostDeleteView, UserPostListView,
    CommentCreateView)

urlpatterns = [
    path('', PostListView.as_view(), name = 'thefav'),
    path('user/<str:username>/', UserPostListView.as_view(), name = 'userposts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'delete'),
    path('post/new/', PostCreateView.as_view(), name = 'create'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name = 'comment'),
    path('about/', views.about, name = 'thefavabout')
    
] 