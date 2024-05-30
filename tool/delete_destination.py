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
from travel.models import Destination

def delete_travel_destinations_starting_from_id(start_id):
    ''' 批量删除 travel_destination 数据，从指定的 ID 开始 '''
    # 使用 filter 函数找到所有 ID 大于等于 start_id 的 travel_destination 对象
    destinations_to_delete = Destination.objects.filter(id__gte=start_id)

    # 删除找到的 travel_destination 对象
    deleted_count, _ = destinations_to_delete.delete()

    print(f"Deleted {deleted_count} travel destinations starting from ID {start_id}.")

if __name__ == "__main__":
    # 设置要开始删除的 ID
    start_id = 10
    delete_travel_destinations_starting_from_id(start_id)
