from .models import User

role = {
    1:"team",
    2:"intern",
    3:"panel",
    4:"guide",
}

def isTeam(user):
    if(user.user_type == User.TEAM):
        return True
    return False

def isIntern(user):
    if(user.user_type == User.INTERN):
        return True
    return False

def isPanel(user):
    if(user.user_type == User.PANEL):
        return True
    return False

def isGuide(user):
    if(user.user_type == User.GUIDE):
        return True
    return False

def isSuperUser(user):
    return user.is_superuser