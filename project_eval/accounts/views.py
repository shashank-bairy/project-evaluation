from django.db.models import Max
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from .models import *
from core.models import User
from marks.models import Rubrics
from django.views import View
from django.contrib.auth.decorators import login_required

class TeamInternSignUpView(View):
  template_name = 'accounts/team_intern_signup_form.html'

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

  def post(self, request, *args, **kwargs):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if User.objects.filter(username=username).exists():
      context = {
        'error': 'User with that username exists.'
      }
      return render(request, self.template_name, context) 

    user_type = int(request.POST.get('user_type'))
    u = User.objects.create(username=username, password=password, user_type=user_type)
    u.set_password(password)
    u.save()
    
    member_team = None
    member_intern = None
    team_strength = 1
    is_intern = False
    if user_type == User.TEAM:
      topic = request.POST.get('topic')
      member_team = Team.objects.create(user=u, topic=topic)
      team_strength = int(request.POST.get('team_strength'))
      
    if user_type == User.INTERN:
      company_name = request.POST.get('company_name')
      member_intern = Intern.objects.create(user=u, company_name=company_name)
      is_intern=True

    for c in range(1, team_strength+1):
      first_name = request.POST.get(f'first_name{c}')
      last_name = request.POST.get(f'last_name{c}')
      usn = request.POST.get(f'usn{c}')
      email = request.POST.get(f'email{c}')
      ph_no = int(request.POST.get(f'ph_no{c}'))
      s = Student.objects.create(
        member_team=member_team,
        member_intern=member_intern,
        usn=usn,
        first_name=first_name,
        last_name=last_name,
        email=email,
        ph_no=ph_no,
        is_intern=is_intern
      )      
    print(request.POST)
    return redirect('/login')

class PanelGuideSignUpView(View):
  template_name = 'accounts/panel_guide_signup_form.html'

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

  def post(self, request, *args, **kwargs):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if User.objects.filter(username=username).exists():
      context = {
        'error': 'User with that username exists.'
      }
      return render(request, self.template_name, context)

    user_type = int(request.POST.get('user_type'))
    u = User.objects.create(username=username, password=password, user_type=user_type)
    u.set_password(password)
    u.save()
    
    member_panel = None
    member_guide = None
    panel_strength = 1
    is_guide = False
    if user_type == User.PANEL:
      member_panel = Panel.objects.create(user=u)
      panel_strength = int(request.POST.get('panel_strength'))
      
    if user_type == User.GUIDE:
      is_external = False
      guide_type = request.POST.get('guide_type1')
      if guide_type == 'ext':
        is_external = True
      member_guide = Guide.objects.create(user=u, is_external=is_external)
      is_guide = True

    for c in range(1, panel_strength+1):
      first_name = request.POST.get(f'first_name{c}')
      last_name = request.POST.get(f'last_name{c}')
      email = request.POST.get(f'email{c}')
      ph_no = int(request.POST.get(f'ph_no{c}'))
      s = Faculty.objects.create(
        member_guide=member_guide,
        member_panel=member_panel,
        first_name=first_name,
        last_name=last_name,
        email=email,
        ph_no=ph_no,
        is_guide=is_guide
      )      
    print(request.POST)
    return render(request, self.template_name)

class LoginInView(View):
  template_name = 'accounts/welcome.html'

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('/dashboard')
    else:
      return render(request, self.template_name)

  def post(self, request, *args, **kwargs):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/dashboard')
    else:
      context = {
        'error': 'Invalid username or password. Please re-enter.'
      }
      return render(request, self.template_name, context)

class GuideSelectView(View):
  template_name = 'accounts/guide_select.html'
  def get(self, request, *args, **kwargs):
    if hasattr(request.user, 'team'):
      if request.user.team.int_guide is not None:
        int_guide = request.user.team.int_guide.guide_faculties.first().full_name
        return render(request, self.template_name, {'input': False, 'int_guides': int_guide })
    if hasattr(request.user, 'intern'):
      if request.user.intern.int_guide is not None:
        int_guide = request.user.intern.int_guide.guide_faculties.first().full_name
        ext_guide = request.user.intern.ext_guide.guide_faculties.first().full_name
        return render(request, self.template_name, {'input': False, 'int_guides': int_guide, 'ext_guides': ext_guide })
    guides = Guide.objects.all()
    int_guides = {}
    ext_guides = {}
    for guide in guides:
      if guide.is_external:
        ext_guides[guide.pk] = guide.guide_faculties.first().full_name
      else:
        int_guides[guide.pk] = guide.guide_faculties.first().full_name
    return render(request, self.template_name, {'input': True, 'int_guides':int_guides,'ext_guides':ext_guides })
  
  def post(self, request, *args, **kwargs):
    if request.user.user_type == User.TEAM:
      team = request.user.team
      ipk = int(request.POST.get('int_guide'))
      int_guide = Guide.objects.get(pk=ipk)
      team.int_guide = int_guide
      team.save()
    if request.user.user_type == User.INTERN:
      intern = request.user.intern
      ipk = int(request.POST.get('int_guide'))
      int_guide = Guide.objects.get(pk=ipk)
      intern.int_guide = int_guide
      epk = int(request.POST.get('ext_guide'))
      ext_guide = Guide.objects.get(pk=epk)
      intern.ext_guide = ext_guide
      intern.save()
    return redirect('/guide_select')

class DashboardView(View):
  template_name = 'accounts/dashboard.html'

  def get(self, request, *args, **kwargs):
    context = {}
    user = request.user
    if hasattr(user, 'team'):
      if user.team.int_guide is not None:
        context['int_guide'] = user.team.int_guide.guide_faculties.first()
      context['students'] = user.team.students.all()
    if hasattr(user, 'intern'):
      if user.intern.int_guide is not None:
        context['int_guide'] = user.intern.int_guide.guide_faculties.first()
      if user.intern.ext_guide is not None:
        context['ext_guide'] = user.intern.ext_guide.guide_faculties.first()
      context['student'] = user.intern.student.all().first()
    if hasattr(user, 'panel'):
      context['panel'] = user.panel
      context['faculties'] = user.panel.panel_faculties.all()
    if hasattr(user, 'guide'):
      context['guide'] = user.guide
      context['faculty'] = user.guide.guide_faculties.all().first()
    if request.user.is_superuser:
      context['num_of_phases'] = range(Rubrics.objects.aggregate(Max('phase'))['phase__max'])
    return render(request, self.template_name, context)

class StudentDetailView(View):
  template_name = 'accounts/student_details.html'

  def get(self, request, *args, **kwargs):
    usn = kwargs.get('usn')
    student = Student.objects.get(usn=usn)
    
    return render(request, self.template_name)

class TeamListView(View):
  template_name = 'accounts/team_list.html'

  def get(self, request, *args, **kwargs):
    context = {}
    context['teams'] = Team.objects.all()
    return render(request, self.template_name, context)

class InternListView(View):
  template_name = 'accounts/intern_list.html'

  def get(self, request, *args, **kwargs):
    context = {}
    context['interns'] = Intern.objects.all()
    return render(request, self.template_name, context)

def team_evaluate(request, id):
  template_name = 'accounts/team_evaluate.html'
  print()
  context = {}
  context['num_of_phases'] = range(Rubrics.objects.aggregate(Max('phase'))['phase__max'])
  context['team'] = Team.objects.get(pk=id)
  context['students'] = context['team'].students.all()
  if context['team'].int_guide is not None:
    context['int_guide'] = context['team'].int_guide.guide_faculties.first()
  return render(request, template_name, context)

def intern_evaluate(request, id):
  template_name = 'accounts/intern_evaluate.html'
  print()
  context = {}
  context['num_of_phases'] = range(Rubrics.objects.aggregate(Max('phase'))['phase__max'])
  context['intern'] = Intern.objects.get(pk=id)
  context['student'] = context['intern'].student.all().first()
  if context['intern'].int_guide is not None:
    context['int_guide'] = context['intern'].int_guide.guide_faculties.first()
  if context['intern'].ext_guide is not None:
    context['ext_guide'] = context['intern'].ext_guide.guide_faculties.first()
  return render(request, template_name, context)

# @login_required
def logout_view(request):
  template_name = 'accounts/logout_success.html'
  logout(request)
  return render(request, template_name)

def dashboard_view(request):
  template_name = 'accounts/dashboard.html'
  return render(request, template_name)

# def welcome_view(request):
#   template_name = 'accounts/welcome.html'
#   if request.user.is_authenticated:
#     return redirect('/dashboard')
#   else:
#     return render(request, template_name)