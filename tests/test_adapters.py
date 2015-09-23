import unittest

from ..adapters import serialize_map_state
from ..domain import Map
from ..settings import DEFAULT_OBJECT


class TestAdapters(unittest.TestCase):
    def test_serialize_map_state(self):
        new_map = Map(DEFAULT_OBJECT)
        map_state = new_map.get_window_range_objects((0, 0), 1)
        serialized_map = serialize_map_state(map_state)
        expected = {
            'map_state': [
                [['Grass'], ['Grass'], ['Grass']],
                [['Grass'], ['Grass'], ['Grass']],
                [['Grass'], ['Grass'], ['Grass']]
            ]
        }

        self.assertDictEqual(expected, serialized_map)
