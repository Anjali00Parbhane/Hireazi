from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.exceptions import ValidationError
from datetime import datetime


class CustomUser(AbstractUser):
    USER = (
        (1,'COORDINATOR'),
        (2,'STUDENT'),
        (3,'MENTOR'),
        (4,'COMPANY'),
    ) 
    user_type = models.CharField(choices=USER, max_length=50,default=1)
    def __str__(self):
        return self.first_name



class College(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    name=models.CharField(max_length=200)
    website=models.CharField(max_length=25)
    # college_type=models.CharField(max_length=10)
    # registration_no=models.IntegerField()
    def __str__(self):
        return self.name
    
    
    
class Department(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name  
    
class ExcelData(models.Model):
    column1 = models.TextField()
    column2 = models.CharField(max_length = 20)
    column3 = models.TextField()
    column4 = models.TextField()

import datetime
def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year


class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    college_name = models.ForeignKey(College, on_delete=models.CASCADE,default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admission_year = models.IntegerField(choices=year_choices,default=current_year)
    university_no=models.IntegerField()
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Domain(models.Model):
    domain_name = models.CharField(max_length=100)
    def __str__(self):
        return self.domain_name




class TechStack(models.Model):
    name=models.CharField(max_length=100)
    logo_image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.name
    



class Timeline(models.Model):
    title = models.CharField(max_length=200)
    admission_year = models.IntegerField(choices=year_choices,default=current_year)
    current_yr = models.IntegerField()
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    college=models.ForeignKey(College,on_delete=models.CASCADE)
    finalize_button_activated=models.BooleanField(default=False)
    def __str__(self):
        return (str(self.title)) 


    

class Mentor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    college_name = models.ForeignKey(College, on_delete=models.CASCADE,default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name=models.CharField(max_length=100, default='')
    def __str__(self):
        return self.name


    
class Panel(models.Model):
    panel_member_1 = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='panel_member_1')
    panel_member_2 = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='panel_member_2')
    panel_member_3 = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='panel_member_3')
    panel_member_4 = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='panel_member_4')
    current_y = models.IntegerField(default=1)
    admission_year = models.IntegerField(choices=year_choices,default=current_year)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Panel {self.id} - {self.department} - {self.current_y}"



    
class Project(models.Model):
    project_title = models.CharField(max_length=200)
    project_domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)
    College=models.ForeignKey(College,on_delete=models.DO_NOTHING,default=1)
    tech_stack=models.ForeignKey(TechStack, on_delete=models.DO_NOTHING)
    member_details_1 = models.ForeignKey(Student,related_name='member_1', on_delete=models.CASCADE,null=True, blank=True)
    member_details_2 = models.ForeignKey(Student,related_name='member_2' ,on_delete=models.CASCADE,null=True, blank=True)
    member_details_3 = models.ForeignKey(Student,related_name='member_3', on_delete=models.CASCADE,null=True, blank=True)
    member_details_4 = models.ForeignKey(Student,related_name='member_4', on_delete=models.CASCADE,null=True, blank=True)
    
    current_yr=models.IntegerField(null=True, blank=True)

    mentor_id=models.ForeignKey(Mentor,on_delete=models.CASCADE,null=True, blank=True)
    timeline_id=models.ForeignKey(Timeline,on_delete=models.CASCADE,null=True, blank=True)
    panel_id = models.ForeignKey(Panel, on_delete=models.SET_NULL, blank=True, null=True)
    
    abstract=models.CharField(max_length=500,blank=True, null=True)
    support_doc = models.FileField(upload_to='documents/', blank=True, null=True)
    image_1 = models.ImageField(upload_to='images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='images/', blank=True, null=True)

    communications_presentation_score=models.IntegerField(null=True, blank=True)
    innovation_score=models.IntegerField(null=True, blank=True)
    coding_standards_score=models.IntegerField(null=True, blank=True)
    societal_score=models.IntegerField(null=True, blank=True)
    national_representation_score=models.IntegerField(null=True, blank=True)

    sponsored=models.BooleanField(default=False)
    published=models.BooleanField(default=False)
    copyrighted=models.BooleanField(default=False)

    def __str__(self):
        return self.project_title
    

class PendingProjectStudentRequest(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    accepted=models.BooleanField(default=False)
    student_no=models.IntegerField()

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    notification_date = models.DateField()
    task_total_score=models.IntegerField()
    def __str__(self):
        return self.name




class TimelineTasks(models.Model):
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
    timeline_title = models.ForeignKey(Timeline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.timeline_title.title} - {self.task_name.name}"




class ProjectTask(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('InProgress', 'In Progress'),
        ('Submitted','Submitted'),
        ('Reassigned','Re Assigned'),
        ('Verified','Verified')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    response = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    score=models.IntegerField(default=0)
    document = models.FileField(upload_to='documents/', blank=True, null=True)

    def clean(self):
        super().clean()
        if self.score < 0 or self.score > self.task_name.task_total_score:
            raise ValidationError('Score must be between 0 and review total score')
    def __str__(self):
        return f"{self.project} - {self.task_name}" 




class Review(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    notification_date = models.DateField()
    review_total_score = models.IntegerField()

    def __str__(self):
        return self.name




class TimelineReview(models.Model):
    review_name = models.ForeignKey(Review, on_delete=models.CASCADE)
    timeline_title = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.timeline_title.title} - {self.review_name}"




class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    review_name = models.ForeignKey(Review, on_delete=models.CASCADE)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    score3 = models.IntegerField()
    score4 = models.IntegerField()   

    def clean(self):
        super().clean()
        for score_field in ['score1', 'score2', 'score3', 'score4']:
            score = getattr(self, score_field)
            if score < 0 or score > self.review_name.review_total_score:
                raise ValidationError(f'{score_field.capitalize()} must be between 0 and review total score')
            
    def __str__(self):
        return f"{self.project} - {self.review_name}"




    
class Company(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    name=models.CharField(max_length=200)
    website=models.CharField(max_length=25)
    # origin_country=models.CharField(max_length=50)
    # regisrtation_no=models.IntegerField()
    def __str__(self):
        return self.name




class CompanyProject(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    project_title = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company_name.name} - {self.project_title.project_title}"
    

