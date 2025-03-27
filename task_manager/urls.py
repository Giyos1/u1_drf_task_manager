from django.urls import path
from task_manager import views
from task_manager.views import ProjectAPIView

# urlpatterns = [
#     path('', views.FirstAPIView.as_view(), name='first'),
#     # path('project', views.ProjectAPIView.as_view(), name='project_list'),
#     path('project/<int:pk>/', views.ProjectAPIView.as_view(), name='project')
# ]
urlpatterns = [
    path("project/", ProjectAPIView.as_view(), name="project_list"),  # GET (hammasi), POST
    path("project/<int:pk>/", ProjectAPIView.as_view(), name="project_detail"),  # GET (bitta), PUT, DELETE
]