import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from travel.models import Category


def user_avatar_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.username}.{ext}'
    path = 'avatars/' + filename
    # 检查文件是否存在并删除
    if default_storage.exists(path):
        default_storage.delete(path)
    return path

class CustomUser(AbstractUser):
    # 已包含字段：username, password, email
    # 添加自定义的字段
    interests = models.ManyToManyField(Category)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    def __str__(self):
        return self.username

    


