import unittest

from ..domain import Character, Map, Obstacle
from ..settings import DEFAULT_OBJECT


class TestCharacter(unittest.TestCase):

    def test_character(self):
        character = Character(1, 2)

        self.assertEqual(character.get_position(), (1, 2))
        self.assertEqual(character.get_type(), 'Character')

    def test_move(self):
        character = Character(0, 0)

        character.move((0, 1))
        self.assertEqual(character.get_position(), (0, 1))

        character.move((0, -1))
        self.assertEqual(character.get_position(), (0, 0))

        character.move((1, 0))
        self.assertEqual(character.get_position(), (1, 0))

        character.move((-1, 0))
        self.assertEqual(character.get_position(), (0, 0))

        character.move((1, 1))
        self.assertEqual(character.get_position(), (1, 1))

        character.move((-1, -1))
        self.assertEqual(character.get_position(), (0, 0))

        character.move((1, -1))
        self.assertEqual(character.get_position(), (1, -1))

        character.move((-1, 1))
        self.assertEqual(character.get_position(), (0, 0))


class TestObstacle(unittest.TestCase):
    def test_obstacle(self):
        tree = 'Tree'
        obstacle = Obstacle(0, 0, tree)

        self.assertEqual(obstacle.get_type(), tree)


class TestMap(unittest.TestCase):
    def test_map(self):
        new_map = Map(DEFAULT_OBJECT)

        self.assertEqual(new_map.get_objects(), [])

    def test_add_characters(self):
        new_map = Map(DEFAULT_OBJECT)
        character = Character(0, 0)
        new_map.add_object(character)

        self.assertEqual(new_map.get_objects(), [character])

    def test_create_default_mapping(self):
        map_range = 5
        new_map = Map(DEFAULT_OBJECT)
        visible_objects = new_map.create_default_mapping((0, 0), map_range)
        previous_y = map_range + 1

        for y in visible_objects:
            previous_x = -map_range - 1
            for x in visible_objects[y]:
                self.assertTrue(previous_x + 1 == x)
                previous_x = x
            self.assertTrue(previous_y - 1 == y)
            previous_y = y

    def test_get_window_range_objects(self):
        tree = 'Tree'
        stone = 'Stone'
        river = 'River'
        new_map = Map(DEFAULT_OBJECT)
        character = Character(0, 0)
        new_map.add_object(character)
        first_obstacle = Obstacle(1, 3, tree)
        new_map.add_object(first_obstacle)
        second_obstacle = Obstacle(-5, 5, stone)
        new_map.add_object(second_obstacle)
        third_obstacle = Obstacle(6, -6, river)
        new_map.add_object(third_obstacle)
        visible_objects = new_map.get_window_range_objects((0, 0), 5)

        self.assertEqual(
            visible_objects[0][0], [DEFAULT_OBJECT, character.type])
        self.assertEqual(visible_objects[3][1], [DEFAULT_OBJECT, tree])
        self.assertEqual(visible_objects[5][-5], [DEFAULT_OBJECT, stone])
        with self.assertRaises(KeyError):
            visible_objects[6][-6]
