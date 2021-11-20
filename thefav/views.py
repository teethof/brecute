from django.contrib.messages.api import success
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, request
from django.urls import reverse_lazy

from .forms import PostCommentForm
from .models import Post, PostComment
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin)
from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView)



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'thefav/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'thefav/home.html' #looking for the template: thefav/post_list.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'thefav/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/thefav/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(CreateView):
    model = PostComment
    template_name='thefav/comment_form.html'
    # fields="__all__"#引入表单form后form中定义了这一行因此可以除去
    form_class = PostCommentForm

    success_url=reverse_lazy('thefav')
    def form_valid(self, form):
        form.instance.post_connected_id = self.kwargs['pk']
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'thefav/about.html',{'title':'about'})
    