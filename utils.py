import math

def one_step(startx, starty, goalx, goaly):
    if startx == goalx:
        if goaly > starty:
            return 0
        elif goaly<starty:
            return 1
    elif starty==goaly:
        if goalx > startx:
            return 3
        elif goalx<startx:
            return 2


def encode_direction(startx, starty, goalx, goaly):
    """
    从start走到goal，对应的退避编码
    :param startx:
    :param starty:
    :param goalx:
    :param goaly:
    :return:
    """
    if startx == goalx:
        if goaly > starty:
            return (1, 0, 0, -1)
        else:
            return (1, 0, 0, 1)
    else:
        if goalx > startx:
            return (0, 1, -1, 0)
        else:
            return (0, 1, 1, 0)


def find_neighbors(robot_pos, start):
    motions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = [(start[0] + u[0], start[1] + u[1]) for u in motions]
    t = []
    for i in neighbors:
        if i in robot_pos:
            t.append(i)
    return t

def euclidean(point1, point2):
    # 计算欧式距离
    if isinstance(point1, (list, tuple)):
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])
    else:
        return math.hypot(point1.x - point2.x, point1.y - point2.y)

def obs_map(maps):
    """
    Initialize obstacles' positions
    :return: map of obstacles
    """
    obs = set()
    for i in range(len(maps)):
        for j in range(len(maps[i])):
            if maps[i][j] != '.' and maps[i][j] != 'B':
                obs.add((i, j))
    return obs