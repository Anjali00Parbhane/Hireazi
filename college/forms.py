from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['college_name', 'department', 'admission_year', 'university_no', 'name']

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['title', 'admission_year', 'current_yr', 'dept']
        

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'notification_date','task_total_score']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notification_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task  # Default model is Task
#         fields = ['name', 'description', 'due_date', 'notification_date', 'task_total_score']
#         widgets = {
#             'due_date': forms.DateInput(attrs={'type': 'date'}),
#             'notification_date': forms.DateInput(attrs={'type': 'date'}),
#             # Add widgets for other fields as needed
#         }

#     # Override the __init__ method to dynamically change the model
#     def __init__(self, *args, **kwargs):
#         form_type = kwargs.pop('form_type', 'task') 
#          # Default form type is 'task'
#         if form_type == 'task':
#             print("anjali")
#             self.Meta.model = Task
#         elif form_type == 'review':
#             self.Meta.model = Review
#         super(TaskForm, self).__init__(*args, **kwargs)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'description', 'due_date', 'notification_date', 'review_total_score']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notification_date': forms.DateInput(attrs={'type': 'date'})
        }
        
class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = [ 'remark','score']


class StudentFilterForm(forms.ModelForm):

    class Meta:
        model=Student
        fields=['admission_year','department']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['abstract', 'support_doc','communications_presentation_score','innovation_score','coding_standards_score','societal_score','national_representation_score' , 'image_1','image_2']

class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['panel_member_1', 'panel_member_2', 'panel_member_3', 'panel_member_4','current_y','admission_year', 'department']

class ProjecteditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'project_domain', 'tech_stack', 'member_details_1', 'member_details_2', 'member_details_3', 'member_details_4', 'current_yr', 'mentor_id', 'timeline_id', 'communications_presentation_score', 'innovation_score', 'coding_standards_score', 'societal_score', 'national_representation_score', 'sponsored']
        
class DocumentForm(forms.Form):
    document = forms.FileField(label='Upload Document')
    
    
    