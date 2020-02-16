from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, username, password, **extra_fields):
    """
    Creates and saves a User with the username and password.
    """
    if not username:
        raise ValueError('Username field cannot be empty.')
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(username, password, **extra_fields)

  def create_superuser(self, username, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError(_('Superuser must have is_staff=True.'))
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')
    return self._create_user(username, password, **extra_fields)