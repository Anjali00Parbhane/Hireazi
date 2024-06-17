import random
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.http import HttpResponseNotAllowed
from college.EmailBackend import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from college.models import *
from .forms import *
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings


def all_login(request):
    if request.method == "POST":
        user = EmailBackend.authenticate(request,
                                           username=request.POST.get('email'),
                                           password=request.POST.get('password'),)
        if user!=None:
            login(request,user)
            user_type = user.user_type
            print(user_type)
            if user_type == '1':
                return redirect('home')
            elif user_type == '2':
                return redirect('student_explore')
            elif user_type == '3':
                return redirect('mentor_projects')
            elif user_type == '4':

                return redirect('company_explore')
            else:
                messages.error(request,'Email and password are invalid')
                return HttpResponse('error')
     
        else:
            print('no user')
            messages.error(request,'Email and password are invalid')
    return render(request,'welcome/login.html')

def home(request):
    return render(request,'Coordinator/index.html')

def welcome_page(request):
     return render(request,'welcome/welcome_page.html')

def logout_view(request):
     logout(request)
     return redirect('welcome_page')

def register_user(request):
    #  if request.method == "POST":
    #     first_name = request.POST.get('first_name')
    #     address = request.POST.get('address')
    #     email = request.POST.get('email')
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     website=request.POST.get('website')
    #     choice=request.POST.get('user_type')

    #     if CustomUser.objects.filter(email=email).exists():
    #       messages.warning(request, 'Email already exist') 
    #       return redirect('register_college')
        
    #     if CustomUser.objects.filter(username=username).exists():
    #       messages.warning(request, 'Username already exist') 
    #       return redirect('register_college')
        
    #     else:
    #         if(choice=='college'):
    #             user_t=1
    #         else:
    #             user_t=4
    #         user = CustomUser(
    #             first_name = first_name,
    #             email = email,
    #             username = username,
    #             password = password,
    #             user_type = user_t,
    #         )

    #         user.set_password(password)
            

    #         if(choice=='college'):
    #             college = College(
    #                 admin = user,
    #                 address = address,
    #                 name=first_name,
    #                 website=website,
    #             ) 
    #             user.save()
    #             college.save()
    #             messages.success(request, 'College registered successfully')
    #             return redirect('login')
    #         elif(choice=='company'):
    #             company = Company(
    #                 admin = user,
    #                 address = address,
    #                 name=first_name,
    #                 website=website,
    #             ) 
    #             user.save()
    #             company.save()
    #             messages.success(request, 'Company registered successfully')
    #             return redirect('login')
     
    #  return render(request,'welcome/register_college.html') 
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        website = request.POST.get('website')
        choice=request.POST.get('user_type')
        request.session['first_name'] = first_name
        request.session['address'] = address
        request.session['email'] = email
        request.session['username'] = username
        request.session['password'] = password1
        request.session['website'] = website
        request.session['user_type'] = choice
        print("1")
        if password1 == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exist') 
                return redirect('register_college')
            
            elif CustomUser.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exist')
                return redirect('register_college')
            else:
                send_otp(request)
                print("2")
                print(request.POST)
                return render(request,'welcome/otp.html', {'email':email})
                 
        else:
            messages.info(request,"password mismatch")
            return redirect('register_college')
    return render(request,'welcome/register_college.html') 

def send_otp(request):
    s=""
    for x in range(0,4):
      s+=str(random.randint(0,9))
        
    request.session["otp"]=s
        
    send_mail("otp for sign up", s, 'hireziarsv@gmail.com', [request.session['email']],fail_silently=False)
        
    return render(request, "welcome/otp.html")

def otp_verification(request):
    if request.method=='POST':
        otp_=request.POST.get("otp")

        if otp_==request.POST.get("otp"):
            encryptedpassword=make_password(request.session['password'])
            

            if(request.session['user_type'] == 'college'):
                user_t=1
            else:
                user_t=4

            nameuser=CustomUser(
                first_name = request.session['first_name'],
                email = request.session['email'],
                username = request.session['username'],
                password = encryptedpassword,
                user_type = user_t)
            nameuser.save()
            
            if(request.session['user_type'] == 'college'):
                college = College(
                admin = nameuser,
                address=request.session['address'],
                name = request.session['first_name'],
                website = request.session['website'] )
                college.save()
                # CustomUser.is_active=True
                messages.success(request,'College registered successfully')
                # return redirect('login')
            else:
                company = Company(
                admin = nameuser,
                address=request.session['address'],
                name = request.session['first_name'],
                website = request.session['website'])
                company.save()
                messages.success(request,'Company registered successfully')
                # return redirect('login')

        

            del request.session['first_name']
            del request.session['address']
            del request.session['email']
            del request.session['username']
            del request.session['password']
            del request.session['user_type']
            del request.session['website']
            del request.session['otp'] 

            CustomUser.is_active=True
            messages.info(request, 'signed in successfully...')
            return redirect('login')
            
        
        else:
            messages.error(request, "otp doesn't match")
    
            return render(request, 'welcome/otp.html')
    else:
        return HttpResponseNotAllowed(['POST'])






def register_student(request):
    if request.method == "POST":
        first_name = request.POST.get('name')
        department_id = request.POST.get('department')
        admission_year = request.POST.get('admission_year')
        university_no = request.POST.get('university_no')
        email = request.POST.get('email')
        password = request.POST.get('password')

        college_obj = College.objects.get(admin=request.user)
        department_obj = Department.objects.get(id=department_id)

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists') 
            return redirect('register_student')
        
        else:
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                user_type=2
            )

            student = Student.objects.create(
                user=user,
                college_name=college_obj,
                department=department_obj,
                admission_year=admission_year,
                university_no=university_no,
                name=first_name
            )

            messages.success(request, 'Student registered successfully')
            return redirect('register_student')
    departments=Department.objects.all()
    return render(request, 'Coordinator/register_student.html',{'departments':departments})



def register_mentor(request):
    domain=Domain.objects.all()
    if request.method == "POST":
        first_name = request.POST.get('name')
        department = request.POST.get('department')
        domain_id = request.POST.get('domain_id')
        email = request.POST.get('email')
        password = request.POST.get('password')

        college_obj = College.objects.filter(admin=request.user).first()

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('register_mentor')
        else:
            user = CustomUser.objects.create_user(
                first_name=first_name,
                email=email,
                username=email,
                password=password,
                user_type=3,  # Assuming mentor user type is 3
            )
            print("user created")
            mentor = Mentor.objects.create(
                user=user,
                college_name=college_obj,
                department=Department.objects.get(id=department),
                domain_id=Domain.objects.get(id=domain_id),
                name=first_name
            )
            print("mentor created")
            messages.success(request, 'Mentor registered successfully')
            return redirect('register_mentor')
    departments=Department.objects.all()
    return render(request, 'Coordinator/register_mentor.html',{'domains':domain,'departments':departments})

    # return render(request,'Coordinator/register_mentor.html')


def  create_timeline(request):
    if request.method == 'POST':
        form = TimelineForm(request.POST)
        if form.is_valid():
            try:
                projects_to_update = Project.objects.filter(
                    timeline_id__isnull=True,
                    member_details_1__admission_year=form.cleaned_data['admission_year'],
                    current_yr=form.cleaned_data['current_yr'],
                    member_details_1__department=form.cleaned_data['dept']
               )
                print(projects_to_update)
                timeline = form.save(commit=False)
                username = request.user
                college=College.objects.get(admin=username)
                print(college)
                timeline.college=college
                timeline.save()
                for project in projects_to_update:
                    project.timeline_id=timeline
                    project.save() 
                
                return redirect('select_to_add_task_or_review',timeline.id)
                # return redirect('add_tasks_to_timeline', timeline_id=timeline.id)
            except Project.DoesNotExist:
                return HttpResponse("No projects found matching the provided criteria.")
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
    else:
        form = TimelineForm()
    return render(request, 'Coordinator/create_timeline.html', {'form': form})

def add_tasks_to_timeline(request, timeline_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task=form.save()
            task_name = form.cleaned_data['name']
            score=form.cleaned_data['task_total_score']
            task = Task.objects.get(id=task.id)
            timeline_task = TimelineTasks.objects.create(
                task_name=task,
                timeline_title_id=timeline_id
            )
            projects_to_update = Project.objects.filter(timeline_id=timeline_id)
            print(projects_to_update)
            for project in projects_to_update:
                    project_task=ProjectTask.objects.create(
                        task_name=task,
                        project=project,
                        score=0
                    )
                    project_task.save() 

            return redirect('add_tasks_to_timeline', timeline_id=timeline_id)
    else:
        form = TaskForm()
    return render(request, 'Coordinator/add_tasks.html', {'form': form})

def add_review_to_timeline(request, timeline_id):
    if request.method == 'POST':
        print(timeline_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            review_name = form.cleaned_data['name']
            score = form.cleaned_data['review_total_score']
            TimelineReview.objects.create(
                review_name=review,
                timeline_title_id=timeline_id
            )
            projects_to_update = Project.objects.filter(timeline_id=timeline_id)
            print(projects_to_update)
            for project in projects_to_update:
                project_review = ProjectReview.objects.create(
                    review_name=review,
                    project=project,
                    score1=0,
                    score2=0,
                    score3=0,
                    score4=0
                )
                project_review.save() 
            return redirect('add_review_to_timeline', timeline_id=timeline_id)
    else:
        form = ReviewForm()
    return render(request, 'Coordinator/add_review.html', {'form': form})



def select_reviews(request):
    departments=Department.objects.all()
    if request.method == 'POST':
        current_year = request.POST.get('current_year')
        admission_year = request.POST.get('admission_year')
        department_id = request.POST.get('department')

        timeline=Timeline.objects.filter(admission_year=admission_year,current_yr=current_year,dept=department_id)
        timelinereview=TimelineReview.objects.filter(timeline_title__in=timeline)
        review = []
        print(timeline,timelinereview)
        for tl in timelinereview:
            reviews_for_timeline = TimelineReview.objects.filter(timeline_title=tl)
            review.extend(reviews_for_timeline)
        # Filter projects based on current_year, admission_year, and department
        # projects = Project.objects.filter(
        #     member_details_1__admission_year=admission_year,
        #     current_yr=current_year,
        #     member_details_1__department_id=department_id
        # )

        # # Get unique reviews scheduled for the filtered projects
        # reviews = Review.objects.filter(project__in=projects).distinct('id')

        # # Create a dictionary to store project details under each review
        # review_projects = {}
        # for review in reviews:
        #     project_list = Project.objects.filter(
        #         member_details_1__admission_year=admission_year,
        #         current_yr=current_year,
        #         member_details_1__department_id=department_id,
        #         review=review
        #     )
        #     review_projects[review] = project_list

        return render(request, 'Coordinator/select_reviews.html', {'reviews': review,'departments':departments})
    departments=Department.objects.all()
    print(departments)
    return render(request, 'Coordinator/select_reviews.html', {'departments':departments})

def projects_by_college(request):
    username = request.user
    college=College.objects.filter(admin=username)
    projects = Project.objects.filter(College__in=college)
    # if request.method=='POST':
    #     form=ProjectFilterForm(request.POST)
    #     if(form.is_valid()):
    #         admission_year=form.cleaned_data['admission_year']
    #         current_year = form.cleaned_data['current_year']
    #         department = form.cleaned_data['department']
    #         projects=Project.objects.filter(
    #             member_details_1__admission_year=admission_year
    #         )
    return render(request, 'Coordinator/project_data.html', {'projects': projects})

def project_tasks_id(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        reviews=ProjectReview.objects.filter(project=project)
        tasks=ProjectTask.objects.filter(project=project)
    except tasks.DoesNotExist:
        return HttpResponse("Project does not exist")
    return render(request, 'Coordinator/project_status.html', {'project': project, 'tasks': tasks, 'reviews':reviews})

def college_timelines(request):
    # Assuming the logged-in user's college is stored in request.user.college
    username = request.user
    college=College.objects.get(admin=username)
    timelines = Timeline.objects.filter(college=college)
    return render(request, 'Coordinator/college_timelines.html', {'timelines': timelines})

def timeline_tasks(request, timeline_id):
    timeline_tasks = TimelineTasks.objects.filter(timeline_title_id=timeline_id)
    task_names = [task.task_name for task in timeline_tasks]
    timeline_review = TimelineReview.objects.filter(timeline_title_id=timeline_id)
    review_names = [review.review_name for review in timeline_review]
    return render(request, 'Coordinator/timeline_tasks.html', {'timeline_tasks': task_names,'reviews':review_names,'timeline_id':timeline_id})

def filter_students(request):
    if request.method == 'POST':
        form = StudentFilterForm(request.POST)
        if form.is_valid():
            admission_year = form.cleaned_data['admission_year']
            department = form.cleaned_data['department']
            students = Student.objects.filter(admission_year=admission_year,  department=department)
            print(students)
            return render(request,'Coordinator/students_data.html', {'students':students,'form':form})
    else:
        form=StudentFilterForm()
    return render(request, 'Coordinator/students_data.html', {'form': form})



def assign_mentors(request): 
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('mentor_'):
                project_id = key.split('_')[-1]
                mentor_id = value
                project = Project.objects.get(id=project_id)
                mentor = Mentor.objects.get(id=mentor_id)
                project.mentor_id = mentor
                project.save()
                messages.success(request,"Mentor Assigned Successfully")
        return redirect('assign_mentors')
    
    college = College.objects.filter(admin=request.user).first()
    projects = Project.objects.filter(College=college)
    mentors=Mentor.objects.filter(college_name=college)
    mentors_by_domain = {}
    for project in projects:
        domain_mentors = Mentor.objects.filter(domain_id=project.project_domain)
        mentors_by_domain[project] = domain_mentors
    return render(request, 'Coordinator/assign_mentors.html', {'projects': projects, 'mentors': mentors})



def create_panel(request):
    if request.method == 'POST':
        form = PanelForm(request.POST)
        if form.is_valid():
            panel_member_1 = form.cleaned_data['panel_member_1']
            panel_member_2 = form.cleaned_data['panel_member_2']
            panel_member_3 = form.cleaned_data['panel_member_3']
            panel_member_4 = form.cleaned_data['panel_member_4']
            current_year = form.cleaned_data['current_y']
            department = form.cleaned_data['department']
            admission_year = form.cleaned_data['admission_year']
            username = request.user
            college = College.objects.get(admin=username)
            
            existing_panels = Panel.objects.filter(
                current_y=current_year,
                department=department
            ).exclude(pk=None)  

            for member in [panel_member_1, panel_member_2, panel_member_3]:
                assigned_panels = existing_panels.filter(
                Q(panel_member_1=member) | Q(panel_member_2=member) | Q(panel_member_3=member) | Q(panel_member_4=member)
                )
                if assigned_panels.exists():
                    messages.error(request, f"{member} is already assigned to another panel in this year and department.")
                    return redirect('create_panel')

            # Create and save the new Panel object
            panel = Panel(
                panel_member_1=panel_member_1,
                panel_member_2=panel_member_2,
                panel_member_3=panel_member_3,
                panel_member_4=panel_member_4,
                current_y=current_year,
                department=department,
                college=college,
                admission_year=admission_year
            )
            panel.save()
            projects_to_update = Project.objects.filter(
                    panel_id__isnull=True,
                    member_details_1__admission_year=admission_year,
                    current_yr=current_year,
                    member_details_1__department=department,
               )
            projects_with_mentors=projects_to_update.filter(                   
                    Q(mentor_id=panel_member_1) | Q(mentor_id=panel_member_2) | Q(mentor_id=panel_member_3) | Q(mentor_id=panel_member_4)
)
            print(projects_with_mentors)
            for project in projects_with_mentors:
                print(project)
                project.panel_id=panel
                project.save()
            
            return redirect('create_panel')  # Redirect to desired page after successful creation

    else:
        form = PanelForm()

    return render(request, 'Coordinator/create_panel.html', {'form': form})

    # else:
    #     username = request.user
    #     college=College.objects.get(admin=username)
    #     form = PanelForm(initial={'college': college})
    
    # return render(request, 'Coordinator/create_panel.html', {'form': form})

def mentor_projects(request):
    username = request.user    
    mentor_id = Mentor.objects.get(user=username)
    # Retrieve all projects where the mentor is assigned as a mentor
    projects = Project.objects.filter(mentor_id=mentor_id)
    return render(request, 'mentors/mentor_project.html', {'projects': projects})

def project_tasks_mentor(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        print(project)
        tasks=ProjectTask.objects.filter(project=project)
        reviews=ProjectReview.objects.filter(project=project)
    except tasks.DoesNotExist:
        return HttpResponse("Project does not exist")
    return render(request, 'mentors/tasks.html', {'project': project, 'tasks': tasks, 'reviews':reviews})

# from .forms import DocumentForm  # Import your form (explained later)
# import requests
# import chardet
# from hireazi.utils import extract_text, check_plagiarism_with_copyscape
# import textdistance

# def plagiarism_check(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = request.FILES['document']
#             try:
#                 text = extract_text(document)
#                 api_username = 'cvaishu129'
#                 api_key = '2naj77gkxruv250l'
#                 result = check_plagiarism_with_copyscape(text, api_username, api_key)
#                 print(result)
#                 return render(request, 'mentors/plagiarism_result.html', {'result': result})
#             except ValueError as e:
#                 form.add_error('document', str(e))
#             except requests.RequestException as e:
#                 form.add_error('document', f'Error checking plagiarism: {e}')
#     else:
#         form = DocumentForm()
#     return render(request, 'mentors/plagiarism_check.html', {'form': form})
    
    
import os
import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from pdfminer.high_level import extract_text
from .forms import DocumentForm  # Ensure you have a form to handle file uploads
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def plagiarismheck(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']
            try:
                # Save the uploaded file to a temporary location
                file_path = default_storage.save('tmp/' + document.name, ContentFile(document.read()))

                # Extract text from the uploaded PDF
                text = extract_text(file_path)
                default_storage.delete(file_path)  # Clean up the temporary file

                # Prepare the API request
                headers = {
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZGY0ZWM5MWEtZWY3YS00ZjY5LWE5MzctNzYyYmRhZTgxOTAwIiwidHlwZSI6ImFwaV90b2tlbiJ9.RifPVZRGLW-vovOBwk0ahrXozqGYDJ5YyK84dfcFRhg",
                    "Content-Type": "application/json"
                }
                url = "https://api.edenai.run/v2/text/plagia_detection"
                payload = {
                    "providers": "originalityai",
                    "text": text,
                    "title": "Your optional title",
                    "fallback_providers": ""
                }

                # Call the Eden AI Plagiarism Detection API
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the API response
                result = response.json()
                plagiarism_results = result.get('originalityai', {}).get('items', [])

                # Render the results
                return render(request, 'mentors/plagiarism_result.html', {'result': plagiarism_results})
            except ValueError as e:
                form.add_error('document', str(e))
            except requests.RequestException as e:
                form.add_error('document', f'Error checking plagiarism: {e}')
    else:
        form = DocumentForm()
    return render(request, 'mentors/plagiarism_check.html', {'form': form})
   
    
    
def task_details_mentor(request, task_id):
    task = ProjectTask.objects.get(id=task_id)
    if request.method == 'POST':
        print(request.POST)
        form = ProjectTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            project_id = task.project.id
            print(project_id)
            # return redirect('project_tasks', project_id=project_id)
        if 'verify' in request.POST:
            task.status = 'Verified'
            task.save()
            return redirect('project_tasks_mentor', project_id=task.project.id)  
            
        elif 'reassign' in request.POST:
            task.status='Reassigned'
            task.save()
            return redirect('project_tasks_mentor', project_id=task.project.id)  
    else:
        form = ProjectTaskForm(instance=task)

    return render(request, 'mentors/task_verify.html', {'task': task, 'form': form})

def review_details_mentor(request,review_id):
    review = ProjectReview.objects.get(id=review_id)
    return render(request, 'mentors/review_details_mentor.html', {'review': review})


def finalize_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('mentor_projects')  # Redirect to a success page
    else:
        form = ProjectForm(instance=project)
    return render(request, 'mentors/finalize_project.html',{'form':form})

def select_to_add_task_or_review(request,timeline_id):
    return render(request,'Coordinator/select_to_add_task_or_review.html',{'timeline_id':timeline_id})


def edit_task(request, task_id,timeline_id):
    task = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # print(form)
            messages.success(request, 'Task edited successfully!')
            return redirect('timeline_tasks', timeline_id)  # Redirect to timeline details
        else:
            for key, errors in form.errors.items():
                print(f"Error in field {key}: {errors}")
    else:
        form = TaskForm(instance=task)

    return render(request, 'Coordinator/edit_task.html', {'form': form})



def edit_review(request, review_id,timeline_id):
    review = Review.objects.get(pk=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        print(request)
        if form.is_valid():
            form.save()
            # print(form)
            messages.success(request, 'Review edited successfully!')
            return redirect('timeline_tasks', timeline_id)  # Redirect to timeline details
        else:
            for key, errors in form.errors.items():
                print(f"Error in field {key}: {errors}")
    else:
        form = ReviewForm(instance=review)

    return render(request, 'Coordinator/edit_review.html', {'form': form})


# def edit_project_view(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     domains=Domain.objects.all()
#     tech_stack=TechStack.objects.all()
#     # Handle form submission if needed
#     return render(request, 'Coordinator/edit_project.html', {'project': project,'domains':domains,})

def edit_project_view(request, project_id):
    # Fetch the project object based on the provided project ID
    project = get_object_or_404(Project, id=project_id)
    username = request.user
    college=College.objects.get(admin=username)
    # Assuming you have models for Domain, TechStack, Mentor, Timeline, and Panel
    domains = Domain.objects.all()
    tech_stacks = TechStack.objects.all()
    students = Student.objects.filter(college_name=college)
    mentors = Mentor.objects.filter(college_name=college)
    timelines = Timeline.objects.filter(college=college)
    panels = Panel.objects.filter(college=college)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ProjectForm(request.POST,  instance=project)
        if form.is_valid():
            form.save()
            print(request.POST)
            return redirect('projects_by_college')
    else:
        # Create a form instance and populate it with the current project data
        form = ProjectForm(instance=project)
        # print(form)
    # Render the HTML template with the form and project data
    return render(request, 'Coordinator/edit_project.html', {'form': form, 'project': project, 'domains': domains, 'tech_stacks': tech_stacks, 'students': students, 'mentors': mentors, 'timelines': timelines, 'panels': panels})



def review_score(request,review_id):
    review=ProjectReview.objects.get(id=review_id)
    username = request.user
    mentor=Mentor.objects.get(user=username)
    try:
        panel = Panel.objects.filter(Q(panel_member_1=mentor) | Q(panel_member_2=mentor) | Q(panel_member_3=mentor) | Q(panel_member_4=mentor)).first()
    except Panel.DoesNotExist:
        panel = None        
    if panel:
        projects = Project.objects.filter(panel_id=panel)
    if request.method == 'POST':
        if panel.panel_member_1 == mentor:
            panel_position = 1
        elif panel.panel_member_2 == mentor:
            panel_position = 2
        elif panel.panel_member_3 == mentor:
            panel_position = 3
        elif panel.panel_member_4 == mentor:
            panel_position = 4
        print(request.POST)
        # for project in projects:
        #     # review=ProjectReview.objects.get(project=project,review_name=review.review_name.id)
        #     # score_field=f'score{panel_position}'
        #     # score_value = request.POST.get(f'score_{project.id}')
        #     # review.{score_field}=request.POST.get('{project}')
        #     review = get_object_or_404(ProjectReview, project=project, review_name=review.review_name)
        #     score_field = f'score{panel_position}'
        #     score_value = request.POST.get(f'score_{project.id}')
        #     setattr(review, score_field, score_value)
        for project in projects:
            score_field = f'score{panel_position}'  # Assuming mentor position is already determined
            project_name = project.project_title  # Assuming the project has a 'name' field
            score_value = request.POST.get(project_name)  # Access score using project name
            review=ProjectReview.objects.get(project=project,review_name=review.review_name.id)
            print("sdsfsd")
            if score_value:
                try:
                    print(score_value,score_field)
                    setattr(review, score_field, int(score_value))
                    review.save()
                    # review.update(**{score_field: score_value})
                    print(review.score1,review.score2,review.score3,review.score4)
                except (ValueError, TypeError) as e:
                    print(f"Error updating score for project {project.name}: {e}")
                    return HttpResponse("score saved")
        return render(request, 'mentors/review_score.html', {'projects': projects,'review_id':review})
    else:
        return render(request, 'mentors/review_score.html', {'projects': projects,'review_id':review})




def review_detail_mentor(request):
    username = request.user
    mentor=Mentor.objects.get(user=username)
    if mentor:
        try:
            panel = Panel.objects.filter(Q(panel_member_1=mentor) | Q(panel_member_2=mentor) | Q(panel_member_3=mentor) | Q(panel_member_4=mentor)).first()
        except Panel.DoesNotExist:
            return HttpResponse("Panel is not assigned till now.")
    projectreview=ProjectReview.objects.filter(project__panel_id=panel.id)
    print(projectreview)
    return render(request, 'mentors/review_details.html', {'projectreview': projectreview})




from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import ExcelData
import pandas as pd

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']

            # Read Excel file using pandas
            df = pd.read_excel(excel_file)

            # Save each row to the database
            for index, row in df.iterrows():
                ExcelData.objects.create(
                    column1=row['column1'],
                    column2=row['column2'],
                    column3 =row['column3'],
                    column4 = row['column4']
                    # Map other fields accordingly
                )
                print(row['column1'])    

            return HttpResponse("SUCEESFULLY EXECUTED!!!!!!!")  
        
    else:
        form = ExcelUploadForm()

    return render(request, 'Coordinator/upload_excel.html',{'form':form})


import os
from django.conf import settings
from django.shortcuts import render
from .forms import DocumentForm
from pdfminer.high_level import extract_text
from io import BytesIO
import textdistance

def plagiarism_check(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']

            # Convert the uploaded document to a byte stream
            document_bytes = document.read()
            document_stream = BytesIO(document_bytes)

            # Extract text from the PDF document
            text = extract_text(document_stream)

            # For demonstration, we use a predefined text to compare against
            predefined_text = "This is a sample text for plagiarism detection."

            # Calculate Jaccard similarity
            similarity_score = textdistance.jaccard.normalized_similarity(text, predefined_text)
            result = {
                'similarity_score': similarity_score,
                'is_plagiarized': similarity_score > 0.5  # Example threshold
            }

            return render(request, 'mentors/plagiarism_result.html', {'result': result})
    else:
        form = DocumentForm()
    return render(request, 'mentors/plagiarism_check.html', {'form': form})





