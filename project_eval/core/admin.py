from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import CustomUserCreationForm ,CustomUserChangeForm 

class UserAdmin(BaseUserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = User

  list_display = ('username', 'user_type', 'is_staff', 'is_active',)
  list_filter = ('username', 'user_type','is_staff', 'is_active',)
  fieldsets = (
    (None, {'fields': ('username', 'user_type', 'password')}),
    ('Permissions', {'fields': ('is_staff','is_active',)}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('username','user_type', 'password1', 'password2', 'is_staff', 'is_active')
    }),
  )
  search_fields = ('username',)
  ordering = ('username',)

# Register your models here.
admin.site.register(User, UserAdmin)