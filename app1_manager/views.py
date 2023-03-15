from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from app1_manager.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError


@login_required
def home(request):
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
    # GET - request resource from server & POST - submit data to server
    if request.method == 'GET':
        # UserCreationForm : built-in Django form used for user registration
        return render(request, 'app1_manager/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('post_list')
            except IntegrityError:
                return render(request, 'app1_manager/signup.html',
                              {'form': UserCreationForm(), 'error': 'That username has already been taken. Please '
                                                                    'choose a new username'})

        else:
            return render(request, 'app1_manager/signup.html', {'form': UserCreationForm(), 'error': 'Passwords did not '
                                                                'match'})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'app1_manager/posts.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'app1_manager/post_detail.html', context)
