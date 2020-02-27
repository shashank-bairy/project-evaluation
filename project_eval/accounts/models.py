from django.db import models
from core.models import User

class Guide(models.Model):
  user = models.OneToOneField(User,related_name='guide', on_delete=models.CASCADE)
  is_external = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username

class Panel(models.Model):
  user = models.OneToOneField(User,related_name='panel', on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username
    
class Faculty(models.Model):  
  member_panel = models.ForeignKey(Panel, related_name='panel_faculties',null=True, blank=True, on_delete=models.CASCADE)
  member_guide = models.ForeignKey(Guide, related_name='guide_faculties',null=True, blank=True, on_delete=models.CASCADE)
  is_guide = models.BooleanField(default=False)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=100, unique=True)
  ph_no = models.PositiveIntegerField()
  
  @property
  def full_name(self):
    return self.first_name + ' ' + self.last_name 

  def __str__(self):
    return self.full_name

  @property
  def member(self):
    if self.member_panel_id is not None:
      return self.member_panel
    if self.member_guide_id is not None:
      return self.member_guide
    raise AssertionError("Neither 'member_panel' nor 'member_guide' is set")

class Team(models.Model):
  user = models.OneToOneField(User,related_name='team',on_delete=models.CASCADE)
  topic = models.CharField(max_length=255)
  int_guide = models.ForeignKey(Guide, related_name='t_int_guide',null=True,blank=True,on_delete=models.SET_NULL)

  @property
  def num_of_students(self):
    return students.count()

  def __str__(self):
    return self.user.username

class Intern(models.Model):
  user = models.OneToOneField(User,related_name='intern', on_delete=models.CASCADE)
  company_name = models.CharField(max_length=50)
  int_guide = models.ForeignKey(Guide, related_name='i_int_guide', null=True, blank=True, on_delete=models.SET_NULL)
  ext_guide = models.ForeignKey(Guide, related_name='i_ext_guide', null=True, blank=True, on_delete=models.SET_NULL)

  def __str__(self):
    return self.user.username

class Student(models.Model):
  usn = models.CharField(max_length=20, unique=True, primary_key=True)
  member_team = models.ForeignKey(Team,related_name='students', null=True, blank=True, on_delete=models.CASCADE)
  member_intern = models.ForeignKey(Intern,related_name='student',null=True, blank=True, on_delete=models.CASCADE)
  is_intern = models.BooleanField(default=False)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=100, unique=True)
  ph_no = models.PositiveIntegerField()
  
  @property
  def full_name(self):
    return self.first_name + ' ' + self.last_name 

  def __str__(self):
    return self.full_name

  @property
  def member(self):
    if self.member_team_id is not None:
      return self.member_team
    if self.member_intern_id is not None:
      return self.member_intern
    raise AssertionError("Neither 'member_team' nor 'member_intern' is set")


# class Member(models.Model):
#   first_name = models.CharField(max_length=50)
#   last_name = models.CharField(max_length=50)
#   email = models.EmailField(max_length=100, unique=True)
#   ph_no = models.PositiveIntegerField()
  
#   @property
#   def full_name(self):
#     return self.first_name + ' ' + self.last_name 

#   def __str__(self):
#     return self.full_name