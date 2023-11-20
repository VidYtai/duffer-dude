from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from tinymce.models import HTMLField


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = HTMLField()
    views = models.IntegerField(default=0)
    slug = models.CharField(max_length=200, unique=True)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + '... by ' + self.user.username
