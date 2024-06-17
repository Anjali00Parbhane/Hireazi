
# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from college.models import *
from student.forms import *

def student_explore(request):
    projects = Project.objects.all()
    return render(request, 'students/explore.html', {'projects': projects})

def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    print(project)
    return render(request, 'students/single_project.html', {'project': project})


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            student_obj = Student.objects.get(user=request.user)
            project.member_details_1 = student_obj
            current_y = datetime.datetime.now().year
            project.current_yr = current_y - student_obj.admission_year
            try:
                timeline=Timeline.objects.get(admission_year=student_obj.admission_year, dept=student_obj.department,current_yr=project.current_yr)
                project.timeline_id=timeline
            except:
                pass
            project.save()

            member_university_numbers = [
                form.cleaned_data.get('member_details_2_university_number'),
                form.cleaned_data.get('member_details_3_university_number'),
                form.cleaned_data.get('member_details_4_university_number')
            ]
            
            for index, university_number in enumerate(member_university_numbers, start=2):
                if university_number:
                    student = get_object_or_404(Student, university_no=university_number)
                    PendingProjectStudentRequest.objects.create(
                        student=student,
                        project=project,
                        student_no=index 
                    )

            current_y = datetime.datetime.now().year
            project.current_yr = current_y - student_obj.admission_year
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'students/register_project.html', {'form': form})
def project_list(request):
    current_user = request.user
    print(request.user)
    try:
        student = Student.objects.get(user=current_user)

        projects = Project.objects.filter(member_details_1=student) | \
                   Project.objects.filter(member_details_2=student) | \
                   Project.objects.filter(member_details_3=student) | \
                   Project.objects.filter(member_details_4=student)
    except Student.DoesNotExist:
        return HttpResponse("No student found for the current user.")

    return render(request, 'students/personal_projects.html', {'projects': projects})




def view_project_requests(request):
    student = Student.objects.get(user=request.user)
    pending_requests = PendingProjectStudentRequest.objects.filter(student=student,accepted=False)
    return render(request, 'students/view_project_request.html', {'pending_requests': pending_requests})



def accept_project_request(request, request_id):
    pending_request = get_object_or_404(PendingProjectStudentRequest, id=request_id)
    pending_request.accepted = True
    pending_request.save()
    current_project = pending_request.project
    project=PendingProjectStudentRequest.objects.filter(project=current_project)
    all_requests_accepted=PendingProjectStudentRequest.objects.filter(project=current_project, accepted=False).exists()
    if not all_requests_accepted:
        for request in project:
            if request.student_no == 2:
                current_project.member_details_2 = request.student
            elif request.student_no == 3:
                current_project.member_details_3 = request.student
            elif request.student_no == 4:
                current_project.member_details_4 = request.student
        current_project.save()
    return redirect('view_project_request')



def project_tasks(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        print(project)
        tasks=ProjectTask.objects.filter(project=project)
        print(tasks)
    except tasks.DoesNotExist:
        return HttpResponse("Project does not exist")
    return render(request, 'students/tasks.html', {'project': project, 'tasks': tasks})


def task_details(request, task_id):
    task = ProjectTask.objects.get(id=task_id)
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status='Submitted'
            form.save()
            print(task.project)
            return redirect('project_tasks', project_id=task.project.id)
    else:
        form = ProjectTaskForm(instance=task)
    return render(request, 'students/task_submit.html', {'task': task, 'form': form})



def profile_dashboard(request):
    try:
        student = get_object_or_404(Student, user=request.user)
        projects = Project.objects.filter(member_details_1=student) | \
                   Project.objects.filter(member_details_2=student) | \
                   Project.objects.filter(member_details_3=student) | \
                   Project.objects.filter(member_details_4=student)
    except Student.DoesNotExist:
        return HttpResponse("No student found for the current user.")

    return render(request, 'students/dashboard.html', {'projects': projects,'user':student})