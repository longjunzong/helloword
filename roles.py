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

    def choose_goods(self, goods_list):
        self.aStar.s_goal = (self.x, self.y)
        value_estimate = []
        cant_get=[]
        for i, good in enumerate(goods_list):
            h = abs(good.x - self.x) + abs(good.y - self.y) + 1
            value = -good.val / (h+good.cost)
            if good.TTL > h + 5:
                if not good.is_reserved and good.nearby_berth[0] in self.can_reach_berth:
                    heapq.heappush(value_estimate, (value, i,good.nearby_berth, good.x, good.y))
        if len(value_estimate) > 0:
            path =[]
            while len(path)==0 and len(value_estimate)>0:
                optim = heapq.heappop(value_estimate)
                if optim[0] < self.cost-1:
                    self.aStar.s_start = (optim[-2], optim[-1])
                    path = self.aStar.searching()
                    if len(path)>0:
                        goods_list[optim[1]].is_reserved = True
                        if self.goods == 0 and self.goods_idx != -999:
                            goods_list[self.goods_idx].is_reserved = False
                        self.cost, self.path, self.goods_idx = optim[0], path, optim[1]
                        self.berth_index=optim[2][0]
                    else:
                        cant_get.append(goods_list[optim[1]])
        return cant_get

    def choose_berth(self,goods,berth_pos,berth_index):
        self.aStar.s_goal = (self.x, self.y)
        if len(goods.path)>0:
            self.berth_index, self.path = goods.nearby_berth[0],goods.path
        value_estimate =[]
        self.aStar.s_start = goods.nearby_berth[1]
        path = self.aStar.searching()
        if len(path) > 0:
            self.berth_index, self.path = goods.nearby_berth[0], path
        else:
            for i in berth_index:
                if berth_pos[i] != goods.nearby_berth[1]:
                    h = abs(berth_pos[i][0] - self.x) + abs(berth_pos[i][1] - self.y) + 1
                    heapq.heappush(value_estimate, (h, i,berth_pos[i]))
            if len(value_estimate) > 0:
                while len(path) == 0 and len(value_estimate) > 0:
                    optim = heapq.heappop(value_estimate)
                    self.aStar.s_goal = optim[-1]
                    path = self.aStar.searching()
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
        self.nearby_berth=None
        self.is_reserved = False
        self.path = []
        self.cost=None

    def choose_berth(self, berth_pos, berth_index):
        self.aStar.s_goal = (self.x, self.y)
        distance_estimate = []
        for i in berth_index:
            heapq.heappush(distance_estimate,(abs(berth_pos[i][0] - self.x) + abs(berth_pos[i][1] - self.y),i,berth_pos[i])) #曼哈顿距离，berth下标，berth坐标
        path = []
        while len(path) == 0 and len(distance_estimate) > 0:
            optim = heapq.heappop(distance_estimate)
            if optim[0]<40:
                self.aStar.s_start = berth_pos[optim[1]]
                path = self.aStar.searching()
                if len(path)>0:
                    if len(path)-optim[0]<40:
                        self.path = path
                        self.cost=len(path)
                        self.nearby_berth = (optim[1],optim[2])
                    else:
                        optim = heapq.heappop(distance_estimate)
                        self.cost=optim[0]
                        self.nearby_berth=(optim[1],optim[2])
                        break
            else:
                self.cost=optim[0]
                self.nearby_berth = (optim[1],optim[2])
                break



