from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
  TEAM = 1
  INTERN = 2
  PANEL = 3
  GUIDE = 4
  USER_TYPE_CHOICES = (
    (TEAM, 'team'),
    (INTERN, 'intern'),
    (PANEL, 'panel'),
    (GUIDE, 'guide'),
  )
  username = models.CharField(_('username'),max_length=150,unique=True)
  user_type = models.PositiveSmallIntegerField(_('user type'),choices=USER_TYPE_CHOICES, null=True)
  user_id = models.PositiveIntegerField(_('user id'), blank=True, null=True)
  date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
  is_active = models.BooleanField(_('active'), default=True)
  is_staff = models.BooleanField(_('staff'), default=False)

  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = []

  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def __str__(self):
    return self.username