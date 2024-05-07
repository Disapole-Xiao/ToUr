# 类的定义，暂时使用json，后续使用sqlite会修改
import json

class Map:
    def __init__(self, jsonstr) -> None:
        dic = json.loads(jsonstr)
        self.center = dic["center"]
        self.entrance = dic["entrance"]
        self.attractions = dic["attractions"]
        self.amenities = dic["amenities"]
        self.restaurants = dic["restaurants"]
        self.nodes = dic["nodes"]
        self.adjlist = []
        for node in self.nodes:
            self.adjlist.append(node["adj"])
            del node["adj"]
        
# 测试代码        
if __name__=="__main__":
    map = Map(0)
    print(map.attractions, map.amenities, map.restaurants, map.nodes, map.adjlist, sep='\n\n')