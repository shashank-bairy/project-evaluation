from django.contrib import admin

# Register your models here.
from .models import Rubrics, Marks

admin.site.register(Rubrics)
admin.site.register(Marks)