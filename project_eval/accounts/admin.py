from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Member, Guide, Panel, Faculty, Team, Intern, Student

# Register your models here.
admin.site.register(Member)
admin.site.register(Guide)
admin.site.register(Panel)
admin.site.register(Faculty)
admin.site.register(Team)
admin.site.register(Intern)
admin.site.register(Student)