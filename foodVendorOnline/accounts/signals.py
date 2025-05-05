from .models import User,UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save,sender=User)
def signal_user_to_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user= instance)
    else:
        try:
            user = UserProfile.objects.get(user = instance)
            user.save()
        except:
            UserProfile.objects.create(user=instance)
    