import os
from django.conf import settings
from django.db import models
from django.utils import timezone

def user_avatar_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    # 返回存储的相对路径
    return os.path.join('avatars', filename)

def dest_pic_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    # 返回存储的相对路径
    return os.path.join('destinations', filename)

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    interests = models.TextField(default='{}')  ## 可能还需要修改 json字符串

    def __str__(self):
        return self.username

class Destination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    province = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=dest_pic_path, blank=True, null=True)
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True)
    tags = models.TextField()  ## 可能还需要修改 空格分隔的标签

    def __str__(self):
        return self.name

class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_time = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True)
    location = models.ForeignKey(Destination, on_delete=models.PROTECT)

    def __str__(self):
        return f'title: {self.title} author: {self.author.username}'