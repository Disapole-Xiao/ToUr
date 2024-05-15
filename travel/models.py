from django.core.validators import MaxValueValidator, MinValueValidator

import os
from django.db import models

def dest_pic_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    # 返回存储的相对路径
    return os.path.join('destinations', filename)

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=1, choices={('s', '景区'), ('u','学校')}, default='s')
    province = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=dest_pic_path, blank=True, null=True)
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True, validators=[
            # 限制0~5
            MinValueValidator(0, message="Rating must be at least 0"),
            MaxValueValidator(5, message="Rating cannot be greater than 5"),
        ])
    tags = models.ManyToManyField(Category)
    mapjson = models.TextField(default='{}', help_text="请粘贴地图的json文字") # 存储地图的json文件

    def __str__(self):
        return self.name
    
    # 给定用户的兴趣标签，返回游学地与用户的兴趣匹配度
    def compute_interest_match(self, interest: list) -> float:
        match_count = sum(tag in self.tags for tag in interest)
        interest_match = match_count / len(interest)
        return interest_match