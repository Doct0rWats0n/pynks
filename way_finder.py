import GLOBAL
from pprint import pprint
cache = {}


def get_way(x, y, tar_x, tar_y, map, z_map=None, curpoint=1):
    if map is None:
        raise ValueError('Emply map value')
    elif tar_x is None or tar_y is None:
        raise ValueError('Emply target coords value')
    if (x, y, tar_x, tar_y) in cache:
        return cache[(x, y, tar_x, tar_y)]
    if z_map is None:
        print(map)
        z_map = [[0] * len(map[0]) for _ in range(len(map))]
        z_map[x][y] = 1
    for i in range(len(map)):
        for j in range(len(map[i])):
            if z_map[i][j] == curpoint:
                if i > 0 and z_map[i - 1][j] == 0 and map[i - 1][j] in GLOBAL.OPEN_CELLS:
                    z_map[i - 1][j] = curpoint + 1
                if j > 0 and z_map[i][j - 1] == 0 and map[i][j - 1] in GLOBAL.OPEN_CELLS:
                    z_map[i][j - 1] = curpoint + 1
                if i < len(z_map) - 1 and z_map[i + 1][j] == 0 and map[i + 1][j] in GLOBAL.OPEN_CELLS:
                    z_map[i + 1][j] = curpoint + 1
                if j < len(z_map[i]) - 1 and z_map[i][j + 1] == 0 and map[i][j + 1] in GLOBAL.OPEN_CELLS:
                    z_map[i][j + 1] = curpoint + 1
    if z_map[tar_x][tar_y] == 0:
        curpoint += 1
        pprint(z_map)
        return get_way(x, y, tar_x, tar_y, map, z_map, curpoint)

    print(curpoint)
    way = []
    curpoint = z_map[tar_x][tar_y]
    while curpoint > 1:
        if tar_x > 0 and z_map[tar_x - 1][tar_y] == curpoint - 1:
            tar_x, tar_y = tar_x - 1, tar_y
            # way.append((tar_x, tar_y))
            way.append((1, 0))
        elif tar_x < len(z_map) - 1 and z_map[tar_x + 1][tar_y] == curpoint - 1:
            tar_x, tar_y = tar_x + 1, tar_y
            # way.append((tar_x, tar_y))
            way.append((-1, 0))
        elif tar_y > 0 and z_map[tar_x][tar_y - 1] == curpoint - 1:
            tar_x, tar_y = tar_x, tar_y - 1
            # way.append((tar_x, tar_y))
            way.append((0, 1))
        elif tar_y < len(z_map[tar_x]) - 1 and z_map[tar_x][tar_y + 1] == curpoint - 1:
            tar_x, tar_y = tar_x, tar_y + 1
            # way.append((tar_x, tar_y))
            way.append((0, -1))
        curpoint -= 1
    way = way[::-1]
    cache[(x, y, tar_x, tar_y)] = way
    return way


# map = '''################
# #""....B.B...""#
# #"T....B.B...."#
# #"..BBBBBBBB.."#
# #""..........""#
# #######BB#######
# #~~~~~#BB#~~~~~#
# #######BB#######
# #""..........""#
# #"............"#
# #....""""""....#
# #....""""""....#
# #BBBB..........#
# #BBBB........."#
# #XBBB..P.....""#
# ################'''
# map = tuple(tuple(i) for i in map.split('\n'))
# print(get_way(1, 3, 14, 6, map))
