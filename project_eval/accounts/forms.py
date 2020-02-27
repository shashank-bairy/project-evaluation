from django import forms
from core.forms import CustomUserCreationForm
from django.db import transaction

from core.models import User
from .models import Team, Student

