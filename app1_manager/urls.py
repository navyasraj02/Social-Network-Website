from django.urls import path, include
from . import views

app_name = 'app1_manager'

urlpatterns = [

    path('create/', views.create_post, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/', views.posts, name='post_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup')
]
