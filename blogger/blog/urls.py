from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('', views.home, name='home'),
    path('create/', views.create_blog, name='create'),
    path('blog/<int:id>/', views.read_blog, name='read'),
    path('edit/<int:id>/', views.edit_blog, name='edit'),
    path('delete/<int:id>/', views.delete_blog, name='delete'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]