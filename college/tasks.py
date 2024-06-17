# # myapp/tasks.py
# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Project

# @shared_task
# def send_task_notification_email(task_name, project_ids, due_date):
#     for project_id in project_ids:
#         project = Project.objects.get(id=project_id)
#         students = project.members.all()
#         for student in students:
#             send_mail(
#                 subject=f'Task Notification: {task_name}',
#                 message=f'You have a new task: {task_name} due on {due_date}. Please complete it before the due date.',
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[student.email],
#             )
