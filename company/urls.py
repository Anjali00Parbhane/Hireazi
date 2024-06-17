from django.urls import path,include
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('company_explore/', views.company_explore, name='company_explore'),
    path('company_project/<int:pk>/', views.company_project_detail, name='company_project_detail'),
    path('send_contact_mail/<int:pk>/', views.send_contact_mail, name='send_contact_mail'),
    path('profile_company/', views.profile_dashboard, name='profile_dashboard'),
    path('student/<int:student_id>/', views.student_dashboard, name='student_dashboard'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

