from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin           #importing mixin for CBV same as decorator in FBV
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from blog_app.models import Post,Comment
from blog_app.forms import PostForm,CommentForm,UserCreateForm


class AboutView(TemplateView):
    template_name = 'blog_app/about.html'

class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'                                   #getting login url
    redirect_field_name = 'blog_app/post_detail.html'       #will redirect after create the post
    form_class = PostForm                                   #taking form
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy ('blog_app:post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_draft_list.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter (published_date__isnull='True').order_by('create_date')


########################################
# Comment section views as function view

@login_required
def post_publish(request, pk):
    post = get_object_or_404 (Post, pk=pk)
    post.publish()
    return redirect('blog_app:post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404 (Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404 (Comment, pk=pk)
    comment.approve()
    return redirect('blog_app:post_detail', pk=post.pk)  #pk=comment.post.pk

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404 (Comment, pk=pk)
    post_pk = comment.post.pk                           #we saved post's pk before deleting the comment, so we can use it later
    comment.delete()
    return redirect('blog_app:post_detail', pk=post_pk)
