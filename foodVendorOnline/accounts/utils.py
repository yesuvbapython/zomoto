
def dashboard(user):
    if user.role == 1:
        url = 'cusDashboard'
    elif user.role == 2:
        url = 'venDashboard'
    elif user.role == None and user.is_superuser:
        url = 'admin'
    else:
        url = 'cusDashboard'
    return url