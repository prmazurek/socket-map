from collections import OrderedDict


class MapObject(object):
    """This class represents an object on a map."""
    def __init__(self, x, y):
        self.position = (x, y)
        self.type = 'Map Object'

    def get_position(self):
        return self.position

    def get_type(self):
        return self.type

    def __repr__(self):
        return self.type


class Character(MapObject):
    def __init__(self, x, y):
        super(Character, self).__init__(x, y)
        self.type = 'Character'

    def move(self, new_position):
        self.position = tuple(map(sum, zip(self.position, new_position)))


class Obstacle(MapObject):
    def __init__(self, x, y, object_type):
        super(Obstacle, self).__init__(x, y)
        self.type = object_type


class Map:
    def __init__(self, default_type):
        self.objects = []
        self.default_type = default_type

    def add_object(self, object_to_add):
        self.objects.append(object_to_add)

    def get_objects(self):
        return self.objects

    def create_default_mapping(self, position, window_range):
        """This method creates a dictionary representation of the map
        and sets its default values.
        :param position: tuple (x, y)
        :param window_range: integer
        returns {
            int: {
                int: [object],
                int: [object],
                ...
            },
            int: {
                ...
            },
            ...
        }
        """
        visible_objects = OrderedDict()
        map_range_x = range(
            -window_range + position[0],
            window_range + position[0] + 1
        )
        map_range_y = range(
            window_range + position[1],
            -window_range + position[1] - 1,
            -1
        )
        for y in map_range_y:
            visible_objects[y] = OrderedDict()
            for x in map_range_x:
                visible_objects[y][x] = [
                    str(Obstacle(x, y, self.default_type))
                ]
        return visible_objects

    def get_window_range_objects(self, position, window_range):
        """Adding existing objects to map grid.
        :param position: tuple (x, y)
        :param window_range: integer
        returns {
            int: {
                int: [object],
                int: [object],
                ...
            },
            int: {
                ...
            },
            ...
        }
        """
        visible_objects = self.create_default_mapping(position, window_range)

        for _object in self.objects:
            object_position = _object.get_position()
            in_range_x = (
                (position[0] - window_range) <= object_position[0] <=
                (position[0] + window_range)
            )
            in_range_y = (
                (position[1] - window_range) <= object_position[1] <=
                (position[1] + window_range)
            )
            if in_range_x and in_range_y:
                visible_objects[object_position[1]][object_position[0]].append(
                    _object.type
                )
        return visible_objects
