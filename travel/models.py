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
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True)
    tags = models.ManyToManyField(Category)
    mapjson = models.TextField(default='{}', help_text="请粘贴地图的json文字") # 存储地图的json文件

    def __str__(self):
        return self.name
