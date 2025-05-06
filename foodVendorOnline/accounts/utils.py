from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
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
def send_verification_mail_to_activate(request,user):
    domine = get_current_site(request)
    subject = "Activate your account here"
    message = render_to_string("accounts/emails/send_email.html",{
        'domain':domine,
        'user':user,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    to_mail = user.email
    mail = EmailMessage(subject,message,to=[to_mail])
    mail.send()