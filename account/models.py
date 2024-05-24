import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from travel.models import Category


def user_avatar_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    # 返回存储的相对路径
    return os.path.join('avatars', filename)

class CustomUser(AbstractUser):
    # 已包含字段：username, password, email
    # 添加自定义的字段
    interests = models.ManyToManyField(Category)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    def __str__(self):
        return self.username

    


