from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from .models import *
from core.models import User
from django.views import View
from django.contrib.auth.decorators import login_required

class SignUpView(View):
  template_name = 'accounts/signup_form.html'

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

  def post(self, request, *args, **kwargs):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_type = int(request.POST.get('user_type'))
    u = User.objects.create(username=username, password=password, user_type=user_type)
    u.set_password(password)
    u.save()
    
    member_team = None
    member_intern = None
    team_strength = 1
    if user_type == User.TEAM:
      topic = request.POST.get('topic')
      member_team = Team.objects.create(user=u, topic=topic)
      team_strength = int(request.POST.get('team_strength'))
      
    if user_type == User.INTERN:
      company_name = request.POST.get('company_name')
      member_intern = Intern.objects.create(user=u, company_name=company_name)

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
        ph_no=ph_no
      )      
    print(request.POST)
    return render(request, self.template_name)

class LoginInView(View):
  template_name = 'accounts/login_form.html'

  def get(self, request, *args, **kwargs):
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
      return render(request, self.template_name, {'error': 'Invalid username or password. Please re-enter.'})

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


# @login_required
def logout_view(request):
  template_name = 'accounts/logout_success.html'
  logout(request)
  return render(request, template_name)

def dashboard_view(request):
  template_name = 'accounts/dashboard.html'
  return render(request, template_name)

def welcome_view(request):
  template_name = 'accounts/welcome.html'
  if request.user.is_authenticated:
    return redirect('/dashboard')
  else:
    return render(request, template_name)