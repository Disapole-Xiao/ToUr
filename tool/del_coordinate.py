import json

def del_coordinate(li):
    for item in li:
        item['lon'] = item['coordinate']['lon']
        item['lat'] = item['coordinate']['lat']
        del item['coordinate']

if __name__ == '__main__':
    map_id = 1
    with open(f'static/maps/{map_id}.json', 'r',encoding='utf-8') as f:
        dic = json.load(f)
    del_coordinate(dic['attractions'])
    del_coordinate(dic['amenities'])
    del_coordinate(dic['restaurants'])
    with open(f'static/maps/{map_id}.json', 'w',encoding='utf-8') as f:
        json.dump(dic, f, indent=4, ensure_ascii=False)
    print("Done")
    



