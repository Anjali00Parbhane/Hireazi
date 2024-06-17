from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('login/', views.all_login, name='login'),
    path('home',views.home,name='home'),
    path('register_college/', views.register_user, name='register_college'),
    path('register_student/', views.register_student, name='register_student'),
    path('register_mentor/', views.register_mentor, name='register_mentor'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('', include('student.urls'),name='student_explore'),
    path('', include('company.urls'),name='company_explore'),
    path('create_timeline',views.create_timeline,name='create_timeline'),
    path('create_task/', views.add_tasks_to_timeline, name='create_task'),
    path('projects-data/', views.projects_by_college, name='projects_by_college'),
    path('students-data/',views.filter_students,name='filter_students'),
    path('-data/',views.filter_students,name='filter_students'),
    path('add_tasks/<int:timeline_id>/',views.add_tasks_to_timeline,name='add_tasks_to_timeline'),
    path('add_reviews/<int:timeline_id>/',views.add_review_to_timeline,name='add_review_to_timeline'),
    path('project-tasks-id/<int:project_id>/', views.project_tasks_id, name='project-tasks-id'),
    path('college-timelines/', views.college_timelines, name='college_timelines'),
    path('timeline_tasks/<int:timeline_id>/', views.timeline_tasks, name='timeline_tasks'),
    path('logout/', views.logout_view, name='logout'),
    path('assign-mentors/', views.assign_mentors, name='assign_mentors'),
    path('edit-project/<int:project_id>/', views.edit_project_view, name='edit-project'),
    path('upload/', views.upload_excel, name='upload_excel'),

    # mentor urls
    path('mentor_projects/', views.mentor_projects, name='mentor_projects'),
    path('project/<int:project_id>/tasks_mentor/', views.project_tasks_mentor, name='project_tasks_mentor'),
    path('task-details-mentor/<int:task_id>/', views.task_details_mentor, name='task_details_mentor'),
    path('finalize_project/<int:project_id>', views.finalize_project, name='finalize_project'),
    path('create_panel/', views.create_panel, name='create_panel'),
    path('select_reviews/', views.select_reviews, name='select_reviews'),
    path('select_to_add_task_or_review/<int:timeline_id>',views.select_to_add_task_or_review,name='select_to_add_task_or_review'),
    path('tasks/<int:task_id>/edit/<int:timeline_id>/', views.edit_task, name='edit_task'),
    path('review/<int:review_id>/edit/<int:timeline_id>/', views.edit_review, name='edit_review'),
    path('review_details_mentor/<int:review_id>/', views.review_details_mentor, name='review_details_mentor'),
    path('review_score/<int:review_id>/', views.review_score, name='review_score'),
    path('review_data_mentor/',views.review_detail_mentor,name='review_data_mentor'),
    path('plagiarism_check/', views.plagiarism_check, name='plagiarism_check'),
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)