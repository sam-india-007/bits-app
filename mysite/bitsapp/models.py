from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.urls import reverse
from PIL import Image

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='like')

    @property
    def number_of_likes(self):
        return self.likes.count()
        
    def publish(self):
        self.save()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return '/'

""" class Like(model.Model):
    created_date = models.DateTimeField(default=timezone.now)
    usr = models.ForeignKey(User, related_name = 'user_like')
    ques = models.ForeignKey(Question, related_name = 'question_like') """


class Answer(models.Model):
    ans = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ansrs')
    time = models.DateTimeField(default=timezone.now)
    of = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='allans')


class Profile(models.Model):
    usr = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    dp = models.ImageField(default = 'default.jpg',upload_to = 'profile_pics')

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img=Image.open(self.dp.path)

        if img.height>400 or img.width>400:
            output_size=(400,400)
            img.thumbnail(output_size)
            img.save(self.dp.path)
