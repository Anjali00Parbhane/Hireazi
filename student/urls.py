from django.urls import path
from .import views

urlpatterns = [
    path('student_explore', views.student_explore,name='student_explore'),
    path('add_project/', views.add_project,name='add_project/'),
    # path('', views.get_students_by_department, name='get_students_by_department'),
    path('project/<int:pk>/', views.project_detail_view, name='project_detail'),
    path('project_list',views.project_list,name='project_list'),
    path('project/<int:project_id>/tasks/', views.project_tasks, name='project_tasks'),
    path('task-details/<int:task_id>/', views.task_details, name='task_details'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('view_project_request/',views.view_project_requests,name="view_project_request"),
    path('accept_project_request/<int:request_id>/', views.accept_project_request, name='accept_project_request'),

]