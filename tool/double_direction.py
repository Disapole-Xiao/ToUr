import json
# jstr = '''
# {
#     "nodes": [
#         {
#             "id": 0,
#             "adj": [
#                 {
#                     "id": 1,
#                     "distance": 1
#                 }
#             ]
#         },
#         {
#             "id": 1,
#             "adj": [
#                 {
#                     "id": 2,
#                     "distance": 1
#                 }
#             ]
#         },
#         {
#             "id": 2,
#             "adj": [
#                 {
#                     "id": 0,
#                     "distance": 1
#                 }
#             ]
#         }
#     ]
# }
# '''
# dic = json.loads(jstr, encoding='utf-8')
with open("static/maps/1.json", "r", encoding='utf-8') as f:
    dic = json.load(f)
for node in dic['nodes']:
    for a in node['adj']:
        adj_id = a['id']
        try: 
            adj = dic['nodes'][adj_id]
        except IndexError:
            print(f"Error: node id = {node['id']},adj_id = {adj_id}")
        # 如果没有则添加
        if node['id'] not in [x['id'] for x in adj['adj']]:
            apd = dict(a)
            apd['id'] = node['id']
            adj['adj'].append(apd)

with open("static/maps/1.json", "w", encoding='utf-8') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)
# print(json.dumps(dic, ensure_ascii=False, indent=4))