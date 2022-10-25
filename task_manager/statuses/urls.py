from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path("", views.ShowAllStatuses.as_view(), name="all_statuses"),
    path("create/", views.CreateStatus.as_view(), name="create_status"),
    path("<int:pk>/update/", views.UpdateStatus.as_view(), name="update_status"),
    path("<int:pk>/delete/>", views.DeleteStatus.as_view(), name="delete_status"),
]
