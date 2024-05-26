'''
自动存储对象到数据库
'''
import os
import sys

# 设置 Django 项目根目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# 设置 Django 项目的设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'ToUr.settings'

# 初始化 Django
import django
django.setup()

# 导入你的模型
from travel.models import *  

# 以下写你的代码

def fill_amenity_type():
    ''' 设施类型 '''
    i = 1
    while i <= 10:
        AmenityType.objects.create(name=f"amenity_type_{i}")
        i += 1
    print("amenity_type filled")

if __name__ == "__main__":
    fill_amenity_type()
