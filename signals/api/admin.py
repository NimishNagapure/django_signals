from django.contrib import admin

# Register your models here
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','notify_user','notify_user_timestamp','active']