from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import os

def dest_pic_path(instance, filename):
    ''' 游学地图片存储路径 '''
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    # 返回存储的相对路径
    return os.path.join('destinations', filename)

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)

class Destination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=1, choices={('s', '景区'), ('u','学校')}, default='s')
    province = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
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
    def __hash__(self) -> int:
        return hash(self.name)
    
class AmenityType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)
    
class RestaurantType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)
    
class User:
    def __init__(self, username):
        self.username = username
        # 可以添加更多的属性，如密码、年龄、性别等

    def __str__(self):
        return f"Username: {self.username}\n"

    def save_to_database(self):
        # 这里可以编写将 User 对象保存到数据库的逻辑
        # 示例代码，实际应用中需要根据你的数据库模型进行调整
        print(f"Saving user '{self.username}' to the database...")
