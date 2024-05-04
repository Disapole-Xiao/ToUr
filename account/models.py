import os
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_avatar_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    # 返回存储的相对路径
    return os.path.join('avatars', filename)

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    interests = models.TextField(default='{}')  ## 可能还需要修改 json字符串

    def __str__(self):
        return self.username
