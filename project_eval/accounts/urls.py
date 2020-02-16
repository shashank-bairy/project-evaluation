from django.urls import path, include
from knox import views as knox_views

urlpatterns = [
  path('api/auth', include('knox.urls'))
]