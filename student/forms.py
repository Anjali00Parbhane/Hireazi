# forms.py
from django import forms
from college.models import *

class ProjectForm(forms.ModelForm):
    member_details_2_university_number = forms.IntegerField(required=True,  label='Member 2 University Number')
    member_details_3_university_number = forms.IntegerField(required=True,  label='Member 3 University Number')
    member_details_4_university_number = forms.IntegerField(required=True,  label='Member 4 University Number')

    class Meta:
        model = Project
        fields = ['project_title', 'project_domain', 'tech_stack']
 


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = [ 'response', 'document']

