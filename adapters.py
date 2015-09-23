def serialize_map_state(map_state):
    map_list = []
    for y in map_state:
        x_list = []
        for x in map_state[y]:
            x_list.append(map_state[y][x])
        map_list.append(x_list)
    return {'map_state': map_list}
