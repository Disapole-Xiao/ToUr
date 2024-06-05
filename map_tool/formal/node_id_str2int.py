import json
with open("static/maps/4.json", "r", encoding='utf-8') as f:
    dic = json.load(f)
for node in dic['nodes']:
    node['id'] = int(node['id'])
    for a in node['adj']:
        a['id'] = int(a['id'])

with open("static/maps/4.json", "w", encoding='utf-8') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)