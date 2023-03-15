from django.urls import path, include
from . import views

app_name = 'app1_manager'

urlpatterns = [

    path('create/', views.home, name='post_create'),
    path('signup/', views.signup, name='signup'),
    # path('login/', views.loginuser, name='loginuser'),
    # path('logout/', views.logoutuser, name='logoutuser'),

    path('', views.home, name='home'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('accounts/', include('django.contrib.auth.urls')),


]
