from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

gender_choices = [
    (None, "Select Gender"),
    ("Female", "Female"), 
    ("Male", "Male"),
    ]

class Tag(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=6, choices=gender_choices, default=1)
    email = models.EmailField(max_length=250, blank=False)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=70, blank=True)
    country = models.CharField(max_length=70, blank=True)
    continent = models.CharField(max_length=70, blank=True)
    profile_picture = models.ImageField(upload_to='uploads/pro_picture/', blank=True)
    about = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)


class UserPost(models.Model):
    date_time = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    post_title = models.CharField(max_length=50)
    post_text = models.TextField(max_length=10000)
    post_image = models.ImageField(upload_to='uploads/post_image/', blank=True)
    tag_category = models.ManyToManyField(Tag, blank=True)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    commenter_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)

    def __str__(self):
        return self.user_post.post_title
    
class ChildComment(models.Model):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    commenter_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    child_comment = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.user_post.post_title} --- {self.parent_comment.comment[0:15:]}"