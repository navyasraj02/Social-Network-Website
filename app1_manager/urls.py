from django.urls import path, include
from . import views

app_name = 'app1_manager'

urlpatterns = [

    path('create/', views.create_post, name='create_post'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    # path('logout/', views.logoutuser, name='logoutuser'),

    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('user/search/', views.user_search, name='user_search'),
    path('user_profile/<int:pk>/', views.user_profile, name='user_profile')

]
