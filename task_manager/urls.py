"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task_manager.views import RegisterUser
from task_manager import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.greetings, name='home'),
    path('users/create/', RegisterUser.as_view(), name='register'),
    path('users/delete_all_of_them', views.UserPage.clear_table),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.ShowAllUsers.as_view(), name='all_users'),
    path('users/<int:pk>/update/', views.update_user_data, name='update'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete'),
]
