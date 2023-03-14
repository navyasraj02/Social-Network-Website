from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, SignUpForm
from app1_manager.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('app1_manager:post_detail', pk=post.pk)
        else:
            print(form.errors)
    else:
        form = PostForm()

    # Render either the form or the login template, depending on the request method
    if not request.user.is_authenticated:
        return render(request, 'app1_manager/login.html', {})
    context = {
        'form': form
    }
    return render(request, 'app1_manager/create_post.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('app1_manager:post_list')
    else:
        form = SignUpForm()
    return render(request, 'app1_manager/signup.html', {'form': form})


def posts(request):
    posts = Post.objects.all()
    return render(request, 'app1_manager/posts.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'app1_manager/post_detail.html', context)
