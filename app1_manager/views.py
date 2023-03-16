from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, UserSearchForm
from app1_manager.models import Post
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, authenticate


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

    # Render either login page or create post page
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html', {})
    context = {
        'form': form
    }
    return render(request, 'app1_manager/create_post.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/login.html', {'form': AuthenticationForm(), 'error': 'Username and '
                                                               'password did not '
                                                               'match'})
        else:
            login(request, user)
            return redirect('app1_manager:post_list')


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
                return redirect('app1_manager:user_profile', pk=user.pk)
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


# get_user_model() : returns the currently active user model class
User = get_user_model()


def user_search(request):
    form = UserSearchForm(request.GET or None)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        results = User.objects.filter(username__icontains=query)

    context = {'form': form, 'results': results}
    return render(request, 'app1_manager/user_search.html', context)


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    url = reverse('user_profile', args=[user_id])
    context = {'user': user, 'profile_url': url}
    return render(request, 'app1_manager/user_profile.html', context)
