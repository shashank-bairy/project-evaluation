from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from core.models import User

class Member(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=100, unique=True)
  ph_no = models.PositiveIntegerField()
  
  @property
  def full_name(self):
    return self.first_name + ' ' + self.last_name 

  def __str__(self):
    return self.full_name

class Guide(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  is_external = models.BooleanField(default=False)

class Panel(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
class Faculty(Member):  
  member_panel = models.ForeignKey(Panel, null=True, blank=True, on_delete=models.CASCADE)
  member_guide = models.ForeignKey(Guide, null=True, blank=True, on_delete=models.CASCADE)

  @property
  def member(self):
    if self.member_panel_id is not None:
      return self.member_panel
    if self.member_guide_id is not None:
      return self.member_guide
    raise AssertionError("Neither 'member_panel' nor 'member_guide' is set")

class Team(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  topic = models.CharField(max_length=255)
  int_guide = models.ForeignKey(Guide, related_name='t_int_guide',null=True, on_delete=models.SET_NULL)

  @property
  def num_of_students(self):
    return students.count()

class Intern(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  company_name = models.CharField(max_length=50)
  int_guide = models.ForeignKey(Guide, related_name='i_int_guide', null=True, on_delete=models.SET_NULL)
  ext_guide = models.ForeignKey(Guide, related_name='i_ext_guide', null=True, on_delete=models.SET_NULL)

class Student(Member):
  usn = models.CharField(max_length=20, unique=True, primary_key=True)
  member_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
  member_intern = models.ForeignKey(Intern, null=True, blank=True, on_delete=models.CASCADE)

  @property
  def member(self):
    if self.member_team_id is not None:
      return self.member_team
    if self.member_intern_id is not None:
      return self.member_intern
    raise AssertionError("Neither 'member_team' nor 'member_intern' is set")
