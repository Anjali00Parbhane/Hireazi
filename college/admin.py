from django.contrib import admin

# Register your models here.
from.models import *
from django.contrib.auth.admin import UserAdmin

# admin.site.register(College)
# admin.site.register(Student)
# admin.site.register(Mentor)
class UserModel(UserAdmin):
    list_display = ['username', 'user_type']

admin.site.register(CustomUser,UserModel)
admin.site.register(College)
admin.site.register(Student)
admin.site.register(Domain)
admin.site.register(Project)
admin.site.register(Timeline)
admin.site.register(Mentor)
admin.site.register(Task)
admin.site.register(TimelineTasks)
admin.site.register(ProjectTask)
admin.site.register(TechStack)
admin.site.register(Department)
admin.site.register(Company)
admin.site.register(CompanyProject)
admin.site.register(Panel)
admin.site.register(Review)
admin.site.register(TimelineReview)
admin.site.register(ProjectReview)
admin.site.register(PendingProjectStudentRequest)

