import os
import sys
import random

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
from travel.models import  Destination,User
from diary.models import Diary

def fill_diary_from_txt(filename):
    ''' 从 txt 文件中读取内容，并填充到 Diary 模型中 '''
    destinations = Destination.objects.filter(type='u').order_by('id')
    destination_index=1
    destination_count = destinations.count()
    flag=0
    # 打开文件
    while 1:
        with open(filename, 'r',encoding='utf-8') as file:
            lines = file.readlines()  # 读取所有行内容
            # 遍历文件的每一行
            for i in range(len(lines)):
                # 如果是数字序号的行
                
                if lines[i].strip().isdigit():
                    # 获取数字序号作为 title
                    title = lines[i+1].strip()  # 获取下一行作为 title
                    # 获取内容，包括当前数字序号以后的段落
                    content = lines[i+2].strip()

                    # 随机选择一个 author_id
                    author_id = random.choice([1, 4, 5, 6, 7, 10, 11, 12, 13, 14])

                    # 获取当前目的地对象
                    travel_destination = destinations[destination_index]
                    destination_index = (destination_index + 1)
                    if destination_index > destination_count:
                        flag=1
                        break
                    # 替换 content 中的 {name} 和 location_id
                    content = content.replace('{name}', travel_destination.name)
                    content = content.replace('{location_id}', str(travel_destination.id))

                    print(content)
                    # 创建 Diary 对象并保存到数据库中
                    diary = Diary.objects.create(title=title, content=content, author_id=author_id,location_id=travel_destination.id)
                    print(f"Diary '{title}' created.")
            if flag==1:
                break

if __name__ == "__main__":
    # 假设 txt 文件名为 'diary.txt'，请替换成实际的文件名
    fill_diary_from_txt('tool/diary_university.txt')
