
from django.shortcuts import render,get_object_or_404
from django.core.mail import send_mail
from django.http import JsonResponse
from college.models import *
from django.db.models import F, ExpressionWrapper, fields
from django.db.models import Q,Sum, Max, Case, When, FloatField, F, ExpressionWrapper

# def company_explore(request):
#     projects = Project.objects.all()
#     colleges = College.objects.all()
#     domains = Domain.objects.all()
#     tech_stacks = TechStack.objects.all()

#     filtered_projects = None
#     if request.method == 'GET':
#         college_id = request.GET.get('college')
#         domain_id = request.GET.get('domain')
#         tech_stack_id = request.GET.get('tech_stack')

#         if college_id:
#             projects = projects.filter(College_id=college_id)
#         if domain_id:
#             projects = projects.filter(project_domain=domain_id)
#         if tech_stack_id:
#             projects = projects.filter(tech_stack_id=tech_stack_id)

#         sort_by = request.GET.get('sort_by')
#         if sort_by in ['communications', 'innovation', 'coding_standards', 'societal', 'national_representation']:
#             sort_field = sort_by + '_score'
#             projects = projects.order_by(sort_field)

#         projects = projects.annotate(
#             task_score=Sum('projecttask__score', filter=Q(projecttask__project_id=F('pk'))),
#             review_score=Sum('projectreview__score1', filter=Q(projectreview__project_id=F('pk'))) + Sum('projectreview__score2', filter=Q(projectreview__project_id=F('pk'))) + Sum('projectreview__score3', filter=Q(projectreview__project_id=F('pk'))) + Sum('projectreview__score4', filter=Q(projectreview__project_id=F('pk'))),
#             task_max_score=Sum('projecttask__task_name__task_total_score', filter=Q(projecttask__score__gt=0)),
#             review_max_score=Sum('projectreview__review_name__review_total_score',filter=Q(projectreview__project_id=F('pk')))*4,
#             task_percentage_score=Case(
#                 When(task_score__gt=0, then=F('task_score') * (100 / F('task_max_score'))),
#                 default=0,
#             ),
#             review_percentage_score=Case(
#                 When(review_score__gt=0, then=F('review_score') * (100 / F('review_max_score'))),
#                 default=0,
#             ),
#         )

#         filtered_projects = projects
#         print(filtered_projects)

#     score_variables = [
#         'communications_presentation_score',
#         'innovation_score',
#         'coding_standards_score',
#         'societal_score',
#         'national_representation_score'
#     ]

#     return render(request, 'company/company_explore.html', {
#         'colleges': colleges,
#         'domains': domains,
#         'tech_stacks': tech_stacks,
#         'filtered_projects': filtered_projects,
#         'score_variables': score_variables

#     })

def company_explore(request):
    projects = Project.objects.all()
    colleges = College.objects.all()
    domains = Domain.objects.all()
    tech_stacks = TechStack.objects.all()

    filtered_projects = projects
    if request.method == 'GET':
        college_id = request.GET.get('college')
        domain_id = request.GET.get('domain')
        tech_stack_id = request.GET.get('tech_stack')
        sort_by = request.GET.get('sort_by')

        filter_kwargs = {}  # Create a dictionary to store filter arguments

        if college_id:
            filter_kwargs['College_id'] = college_id
        if domain_id:
            filter_kwargs['project_domain'] = domain_id
        if tech_stack_id:
            filter_kwargs['tech_stack_id'] = tech_stack_id

        # Apply filters using Q objects for dynamic filtering based on selected options
        if filter_kwargs:
            filtered_projects = filtered_projects.filter(Q(**filter_kwargs))
        else:
            filtered_projects=Project.objects.all()

        filtered_projects = filtered_projects.annotate(
            task_score=Sum('projecttask__score', filter=Q(projecttask__project_id=F('pk'))),
            review_score=Sum('projectreview__score1', filter=Q(projectreview__project_id=F('pk'))) + Sum('projectreview__score2', filter=Q(projectreview__project_id=F('pk'))) + Sum('projectreview__score3', filter=Q(projectreview__project_id=F('pk'))) + Sum('projectreview__score4', filter=Q(projectreview__project_id=F('pk'))),
            task_max_score=Sum('projecttask__task_name__task_total_score', filter=Q(projecttask__score__gt=0)),
            review_max_score=Sum('projectreview__review_name__review_total_score',filter=Q(projectreview__project_id=F('pk')))*4,
            task_percentage_score=Case(
                When(task_score__gt=0, then=F('task_score') * (100 / F('task_max_score'))),
                default=0,
            ),
            review_percentage_score=Case(
                When(review_score__gt=0, then=F('review_score') * (100 / F('review_max_score'))),
                default=0,
            ),
            sortable_task_percentage = F('task_percentage_score'),
    sortable_review_percentage = F('review_percentage_score'),
            rubrics_score=F('communications_presentation_score') + F('innovation_score') + F('coding_standards_score') + F('societal_score') + F('national_representation_score'),
        )
        print(filtered_projects)
        # Sorting logic (unchanged)
        # if sort_by in ['communications', 'innovation', 'coding_standards', 'societal', 'national_representation','task','review']:
        #     sort_field = sort_by + '_score'
        #     filtered_projects = filtered_projects.order_by(sort_field)
        print(sort_by)

        # if sort_by in ['communications_presentation', 'innovation', 'coding_standards', 'societal', 'national_representation', 'task_percentage', 'review']:
        #     sort_field = f'{sort_by}_score' if sort_by != 'task_percentage' and sort_by != 'review' else f'sortable_{sort_by}'
        #     filtered_projects = filtered_projects.order_by(sort_field)

        if sort_by in ['communications_presentation', 'innovation', 'coding_standards', 'societal', 'national_representation', 'task_percentage', 'review']:
            sort_field = f'{sort_by}_score'
            filtered_projects = filtered_projects.order_by(sort_field)
        # if sort_by in ['communications_presentation', 'innovation', 'coding_standards', 'societal', 'national_representation', 'task', 'review']:
        #     sort_field = sort_by + '_score'  # Concatenate sort_by with "_score"
        #     print(sort_field, "fghj")
        #     filtered_projects = filtered_projects.order_by(sort_field)
        for project in filtered_projects:
            print(project, project.task_percentage_score,project.task_score)

        filtered_projects = filtered_projects.filter(Q(rubrics_score__isnull=False))  # Or use .exclude()

    score_variables = [
        'communications_presentation',
        'innovation',
        'coding_standards',
        'societal',
        'national_representation'
    ]

    return render(request, 'company/company_explore.html', {
        'colleges': colleges,
        'domains': domains,
        'tech_stacks': tech_stacks,
        'filtered_projects': filtered_projects,
        'score_variables': score_variables
    })


def company_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    return render(request, 'company/company_single_project.html', {'project': project})


from django.contrib.auth.models import User  # Import User model assuming it's in CustomUser


def send_contact_mail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    current_user = request.user
    college_email = project.College.admin.email  # Assuming admin's email is the college's email

    subject = f"Congratulations! Project {project.project_title} Selected for Recruitment by {current_user.username}"  # More attention-grabbing subject

    message = f"""Good Day!

We are thrilled to inform you that your project, "{project.project_title}", has been selected for further recruitment! 

We're impressed with the work you and your team ({", ".join([student.name for student in [project.member_details_1, project.member_details_2, project.member_details_3, project.member_details_4] if student])}) have done on {project.project_title} at {project.College.name}.

This email initiates the recruitment process for your project. We will be contacting you soon to discuss the next steps.

In the meantime, feel free to reach out to us if you have any questions.

Best regards,

The Hireazi Team
"""

    recipients = [college_email]
    for student in [project.member_details_1, project.member_details_2, project.member_details_3, project.member_details_4]:
        if student and student.user.email:
            recipients.append(student.user.email)

    send_mail(subject, message, "hireziarsv@gmail.com", recipients, False)
    return JsonResponse({"status": "success"})


def profile_dashboard(request):
    current_user = request.user
    
    company = Company.objects.get(admin=current_user)
    
    company_projects = CompanyProject.objects.filter(company_name=company)
    
    context = {
        'company': company,
        'company_projects': company_projects,
    }
    return render(request, 'company/company_dashboard.html', context)




# views.py
from django.shortcuts import render, get_object_or_404
from college.models import Student, Project

def student_dashboard(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    projects = Project.objects.filter(
        member_details_1=student
    ) | Project.objects.filter(
        member_details_2=student
    ) | Project.objects.filter(
        member_details_3=student
    ) | Project.objects.filter(
        member_details_4=student
    )
    
    context = {
        'student': student,
        'projects': projects,
    }
    return render(request, 'company/student_dashboard.html', context)
