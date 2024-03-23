import heapq
import math


class Robot:
    def __init__(self, startX=0, startY=0, goods=0, status=0, aStar=None):
        self.x = startX
        self.y = startY
        self.goods = goods
        self.status = status
        self.cost = 1
        self.path = []
        self.goods_idx = -999
        self.aStar = aStar
        self.berth_index = None
        self.can_reach_berth=[] #该船可到达的港口下标
        self.cant_get_goods=[]

    def choose_goods(self, goods_list,goods_pos):
        self.aStar.s_start = (self.x, self.y)
        value_estimate = []
        for i, good in enumerate(goods_list):
            if not good.is_reserved and good.nearby_berth[0] in self.can_reach_berth and i not in self.cant_get_goods:
                #if good.nearby_berth[0]==self.berth_index and len(good.path)!=0:
                #   h=len(good.path)
                #else:
                h = abs(good.x - self.x) + abs(good.y - self.y) + 1
                if good.TTL > h + 15:
                    value = -good.val / (h + good.cost)
                    heapq.heappush(value_estimate, (value, i,good.nearby_berth, good.x, good.y))
        if len(value_estimate) > 0:
            path =[]
            while len(path)==0 and len(value_estimate)>0:
                optim = heapq.heappop(value_estimate)
                #if goods_list[optim[1]].nearby_berth[0]==self.berth_index and len(goods_list[optim[1]].path)!=0:
                #    path=goods_list[optim[1]].path
                #    if (self.x,self.y) not in path:
                #        path=path[:-2]
                #        self.aStar.s_start=path[-1]
                #        path1=self.aStar.searching()
                #        path1.reverse()
                #        path.extend(path1[1:])
                if optim[0] < self.cost-1:
                    self.aStar.s_goal = (optim[-2], optim[-1])
                    path = self.aStar.searching(True)
                    if len(path)>0:
                        path.reverse()
                        idx = goods_pos[path[-1]]
                        goods_list[idx].is_reserved = True
                        #if self.goods == 0 and self.goods_idx != -999:
                        #    goods_list[self.goods_idx].is_reserved = False
                        self.cost, self.path, self.goods_idx = optim[0], path, idx
                    else:
                        self.cant_get_goods.append(optim[1])

    def choose_berth(self,berth_pos,berth_index):
        self.aStar.s_goal = (self.x, self.y)
        #if len(goods.path)>0:
        #    self.berth_index, self.path = goods.nearby_berth[0],goods.path
        value_estimate =[]
        #if len(path) > 0:
        #    self.berth_index, self.path = goods.nearby_berth[0], path
        #else:
        path=[]
        for i in berth_index:
            if i in self.can_reach_berth:
                h = abs(berth_pos[i][0] - self.x) + abs(berth_pos[i][1] - self.y) + 1
                heapq.heappush(value_estimate, (h, i,berth_pos[i]))
        if len(value_estimate) > 0:
            while len(path) == 0 and len(value_estimate) > 0:
                optim = heapq.heappop(value_estimate)
                self.aStar.s_start = optim[-1]
                path = self.aStar.searching(False)
                if len(path) > 0:
                    self.berth_index, self.path = optim[1], path


class Berth:
    def __init__(self, x=0, y=0, transport_time=0, loading_speed=0):
        self.x = x
        self.y = y
        self.transport_time = transport_time
        self.loading_speed = loading_speed
        self.inventory = 0
        self.ship = -1



class Boat:
    def __init__(self, num=0, pos=0, status=0):
        self.num = num
        self.pos = pos
        self.status = status
        self.instruction = None
        self.flag = False#判断船有没有走


class Goods:
    def __init__(self, x=0, y=0, val=0, ttl=1000, a_star=None,birthday=None):
        self.x = x
        self.y = y
        self.val = val
        self.TTL = ttl
        self.birthday=birthday
        self.aStar = a_star
        self.nearby_berth=None #berth下标，berth坐标
        self.is_reserved = False
        self.path = []
        self.cost=None

    def choose_berth(self, berth_pos, berth_index):
        self.aStar.s_goal = (self.x, self.y)
        distance_estimate = []
        for i in berth_index:
            heapq.heappush(distance_estimate,(abs(berth_pos[i][0] - self.x) + abs(berth_pos[i][1] - self.y),i,berth_pos[i])) #曼哈顿距离，berth下标，berth坐标
        path = []
        optim = heapq.heappop(distance_estimate)
        self.cost=optim[0]
        self.nearby_berth = (optim[1],optim[2])




