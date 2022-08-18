from django.db import models
from django.db.models.fields import BooleanField
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.


#signals import

from django.dispatch import receiver 
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed


)


User = settings.AUTH_USER_MODEL

@receiver(pre_save,sender=User)
def user_pre_save_receiver(sender,instance,*args, **kwargs):
    # Before saved in the database
    print(instance.username,instance.id)
    #instance.save()
    #Dont do this --



@receiver(post_save,sender=User)
def user_post_save_receiver(sender,created,instance,*args, **kwargs):
    # After save in the database

    if created:
        print("Send email to ", instance.username)
        instance.save()
    else:
        print(instance.username," was just saved")

    # print(args,kwargs)

# post_save.connect(user_created_handler,sender =User)





class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True,null=True)
    liked = models.ManyToManyField(User,blank=True)
    notify_user = models.BooleanField(default=False)
    notify_user_timestamp = models.DateTimeField(blank=True,null=True,auto_now_add=False)
    active = models.BooleanField(default=True)

@receiver(pre_save,sender=BlogPost)
def blog_post_pre_save(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title) 
        print('Updateed ')
    
@receiver(post_save,sender=BlogPost)
def blog_post_post_save(sender,instance,created,*args,**kwargs):
    if instance.notify_user:
        print('Notify users')
        instance.notify_users = False
        # instance.save()
        instance.notify_user_timestamp=timezone.now()



@receiver(pre_delete,sender=BlogPost)
def blog_post_pre_delete(sender,instance,*args,**kwargs):
    print(f"{instance.id} will deleted")




@receiver(post_delete,sender=BlogPost)
def blog_post_post_delete(sender,instance,*args,**kwargs):
    print(f"{instance.id} has been deleted")



@receiver(m2m_changed,sender=BlogPost.liked.through)
def blog_post_liked_chaged(sender,action,model,pk__set,instance,*args,**kwargs):
    # print(args,kwargs)
    if action == 'pre_add':
        print('was added')
        qs = kwargs.get('model').objects.filter(pk__in=kwargs.get('pk_set'))
        print(qs.count())
