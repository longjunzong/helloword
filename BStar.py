from collections import Counter
from utils import *
import heapq

 
class BStar():
    def __init__(self, obs, N):
        self.obs = obs
        self.N = N
        self.ch=None



    # 获取周围八个点的坐标
    def get_neighbors(self, x, y):
        up = x, y + 1
        down = x, y - 1
        left = x - 1, y
        right = x + 1, y
 
        left_up = x - 1, y + 1
        right_up = x + 1, y + 1
        left_down = x - 1, y - 1
        right_down = x + 1, y - 1
        result = [up, down, left, right, left_up, right_up, left_down, right_down]
        return [p for p in result if 0 <= p[0] < self.N and 0 < p[1] < self.N]
    
     # 获取周围四个点的坐标
    def __get_neighbors(self, x, y):
        up = x, y + 1
        down = x, y - 1
        left = x - 1, y
        right = x + 1, y
 
        result = [up, down, left, right]
        return [p for p in result if 0 <= p[0] < self.N and 0 < p[1] < self.N]

    # 当前点指向终点的向量。 八方向  通过斜率相近得到方向向量（1,0）（-1,0）--（0，-1）（0,1）----(1,1)(-1,-1)---(-1, 1)(1, -1)
    def get_direct(self, start, end):
        x_sub, y_sub = (end[0] - start[0]), (end[1] - start[1])
        # 说明 垂直 x轴上， k = y_sub / x_sub  0为被除数
        if y_sub == 0:
            # 除以绝对值
            return x_sub / abs(x_sub), y_sub
        # 计算斜率
        k = x_sub / y_sub
        # 下或上
        if 3 / 2 < k or k <= -3 / 2:
            if x_sub < 0:
                return (-1, 0)
            else:
                return (1, 0)
        # 左上或右下
        if 1 / 2 < k <= 3 / 2:
            if x_sub < 0:
                return (-1, -1)
            else:
                return (1, 1)
        # 左或右
        if -1 / 2 < k <= 1 / 2:
            if y_sub < 0:
                return (0, -1)
            else:
                return (0, 1)
        # 左下或右上
        if -3 / 2 < k <= -1 / 2:
            if y_sub < 0:
                return (1, -1)
            else:
                return (-1, 1)

    # 爬墙路径
    def obstacle_path(self, start, end, dynamic_obs, closeSet):
        # 穿透点信息
        temp_point=start
        while True:
            # 传进来的点,沿着终点方向，穿透障碍，得到可以探索的第一个点：地图内的任意两点连线都不可能穿过地图边界
            direct=self.get_direct(temp_point, end)
            end_point = temp_point[0] + direct[0], temp_point[1] + direct[1]
            if end_point not in dynamic_obs or end_point == end:
                break
            temp_point = end_point
        # 开启的表,
        openSet = []
        heapq.heapify(openSet)
        heapq.heappush(openSet, (euclidean(start, end), start))
        parent = {start: start}
        # 关闭的表
        while openSet != []:
            # 切换到关闭列表
            _, cur = heapq.heappop(openSet)
            closeSet.add(cur)

            # 如果到达穿透点或当前点到目标的欧式距离更短
            if cur == end_point or euclidean(cur, end) < euclidean(end_point, end):
                break

            neighbors = self.__get_neighbors(cur[0], cur[1])
            # 对当前格相邻的4格中的每一个做判断
            for neighbor in neighbors:
                next_point_info = None
                # 不是障碍物且不在关闭表内，边界判定在获取邻居时做了
                if neighbor not in dynamic_obs and neighbor not in closeSet:
                    neighbors_list = self.get_neighbors(neighbor[0], neighbor[1])
                    for neighbor_neighbor in neighbors_list:
                        # 如果该邻居周围的8个格子里有一个障碍， 说明它在墙边缘，
                        if neighbor_neighbor in dynamic_obs:
                            next_point_info = (euclidean(neighbor, end), neighbor)
                            parent[neighbor] = cur
                            break
                if next_point_info:
                    heapq.heappush(openSet, next_point_info)
        vec1 = (end[0] - start[0], end[1] - start[1])
        vec2 = (end[0] - cur[0], end[1] - cur[1])
        # 用来判断终点是否可达
        if not self.the_same_direct(vec1, vec2):
            return [], None
        path = self.extract_path(parent, start, cur)
        if path:
            return path, cur
        else:
            return [], None
        
    def the_same_direct(self, start, end):
        if start == (0, 0) or end == (0, 0):
            return True
        return start[0] * end[0] + start[1] * end[1] > 0

    def extract_path(self, PARENT, s_start, s_goal):
        path = [s_goal]
        s = s_goal

        while True:
            try:
                s = PARENT[s]
            except:
                return None
            path.append(s)

            if s == s_start:
                break
        return list(reversed(path))

    def searching(self, start, end, dynamic_obs):
        cur = start
        path = [start]
        if start == end or end in self.obs or end in dynamic_obs:
            return []
        if not isinstance(dynamic_obs, set):
            dynamic_obs = set(dynamic_obs)
        current_obs = self.obs.union(dynamic_obs)
        # 加一个列表用于记录已经找到的特殊点
        visited_path = set()
        visited_end = []
        while True:
            direct = self.get_direct(cur, end)
            # 当前点 + 指向终点的指向向量, 相加得到下一个点的坐标
            # 这里需要注意
            next_point = cur[0] + direct[0], cur[1] + direct[1]
            need_climb = False
            if next_point not in current_obs:
                # 如果下个点不是障碍物且可达，则更新信息
                temp_point = None
                if direct[0] == 0 or direct[1] == 0:
                    temp_point = None
                elif direct[0] != 0 and (cur[0] + direct[0], cur[1]) not in current_obs:
                    temp_point = (cur[0] + direct[0], cur[1])
                elif direct[1] != 0 and (cur[0], cur[1] + direct[1]) not in current_obs:
                    temp_point = (cur[0], cur[1] + direct[1])
                else:
                    need_climb = True
                # 如果不需要爬墙
                if not need_climb:
                    if temp_point:
                        path.append(temp_point)
                    path.append(next_point)
                    cur = next_point
            else:
                need_climb = True
            # 爬墙
            if need_climb:
                # 爬过返回路径和穿越点, 没爬过返回 [], 0
                sub_path, end_point = self.obstacle_path(cur, end, current_obs, visited_path)
                if end_point == None or end_point in visited_end:
                    return []
                else:
                    visited_end.append(end_point)
                    visited_path.update(sub_path[1:])
                    path += sub_path[1:]
                    cur = end_point

            # 到达终点
            if cur == end:
                return path
        return []

    def repeated_searching(self, start, end, pre_path, dynamic_obs):
        # 利用
        cur = start
        path = [start]
        if start == end or end in self.obs or end in dynamic_obs:
            return None
        if not isinstance(dynamic_obs, set):
            dynamic_obs = set(dynamic_obs)
        current_obs = self.obs.union(dynamic_obs)
        # 加一个列表用于记录已经找到的特殊点
        visited_path = set()
        visited_end = []
        while True:
            # 判断现在这个点是否已经在已有的路径中
            if cur in pre_path:
                index = pre_path.index(cur)
                path = path + pre_path[index + 1:]
                return path

            direct = self.get_direct(cur, end)
            # 当前点 + 指向终点的指向向量, 相加得到下一个点的坐标
            # 这里需要注意
            next_point = cur[0] + direct[0], cur[1] + direct[1]
            need_climb = False
            if next_point not in current_obs:
                # 如果下个点不是障碍物且可达，则更新信息，这里有对角点和上下左右四个点两类需要处理
                temp_point = None
                if direct[0] == 0 or direct[1] == 0:
                    temp_point = None
                elif direct[0] != 0 and (cur[0] + direct[0], cur[1]) not in current_obs:
                    temp_point = (cur[0] + direct[0], cur[1])
                elif direct[1] != 0 and (cur[0], cur[1] + direct[1]) not in current_obs:
                    temp_point = (cur[0], cur[1] + direct[1])
                else:
                    need_climb = True
                # 如果不需要爬墙
                if not need_climb:
                    if temp_point:
                        path.append(temp_point)
                    path.append(next_point)
                    cur = next_point
            else:
                need_climb = True

            # 爬墙
            if need_climb:
                # 爬过返回路径和穿越点, 没爬过返回 [], 0
                sub_path, end_point = self.obstacle_path(cur, end, current_obs, visited_path)
                if end_point == None or end_point in visited_end:
                    return None
                else:
                    visited_end.append(end_point)
                    visited_path.update(sub_path[1:])
                    path += sub_path[1:]
                    cur = end_point

            # 到达终点
            if cur == end:
                return path
 
