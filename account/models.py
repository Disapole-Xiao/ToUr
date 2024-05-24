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

# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     email = models.EmailField(max_length=50, blank=True, null=True)
#     avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
#     def __str__(self):
#         return self.username

class CustomUser(AbstractUser):
    # 添加自定义的字段
    user_interest = models.IntegerField(blank=True, null=True)

    
   
class Interest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} - {self.category.name} - {self.value}'
    


