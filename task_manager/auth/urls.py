from django.urls import path
from task_manager.auth import views


urlpatterns = [
    path("", views.ShowAllUsers.as_view(), name="all_users"),
    path("create/", views.RegisterUser.as_view(), name="register"),
    path("<int:pk>/update/", views.UpdateUserData.as_view(), name="update_user"),
    path("<int:pk>/delete/", views.DeleteUser.as_view(), name="delete_user"),
]
