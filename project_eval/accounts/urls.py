from django.urls import path, include
from .views import *

urlpatterns = [
  path('signup/', TeamInternSignUpView.as_view(), name='signup'),
  # path('login/', LoginInView.as_view(), name='login'),
  path('guide_select/', GuideSelectView.as_view(), name='guide_select'),
  path('teams/', TeamListView.as_view(), name='team_list'),
  path('interns/', InternListView.as_view(), name='intern_list'),
  path('teams/<int:id>', team_evaluate, name='team_evaluate'),
  path('interns/<int:id>', intern_evaluate, name='intern_evaluate'),
  path('student_details/<str:usn>/', StudentDetailView.as_view(), name='student_details'),
  path('create_panel_guide/', PanelGuideSignUpView.as_view(), name='create_panel_guide'),
  path('logout/', logout_view, name='logout'),
  path('dashboard/', DashboardView.as_view(), name='dashboard'),
  path('', LoginInView.as_view(), name='welcome')
]