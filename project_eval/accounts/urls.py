from django.urls import path, include
from .views import *

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('login/', LoginInView.as_view(), name='login'),
  path('guide_select/', GuideSelectView.as_view(), name='guide_select'),
  path('logout/', logout_view, name='logout'),
  path('dashboard/', dashboard_view, name='dashboard'),
  path('', welcome_view, name='welcome')
]