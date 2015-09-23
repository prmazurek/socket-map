import tornado.ioloop
from tornado.options import parse_command_line
from tornado import web, websocket
import json
from random import randint

from domain import Map, Character
from adapters import serialize_map_state
from settings import DIRECTIONS, WINDOW_RANGE, DEFAULT_OBJECT, PORT

cl = []


class IndexHandler(web.RequestHandler):

    def get(self):
        self.render("index.html")


class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def get_map_state(self, character):
        map_state = new_map.get_window_range_objects(
            character.get_position(),
            WINDOW_RANGE
        )
        return serialize_map_state(map_state)

    def open(self):
        if self not in cl:
            character = Character(randint(-10, 10), randint(-10, 10))
            new_map.add_object(character)
            self.character = character
            cl.append(self)
            self.write_message(self.get_map_state(character))

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
        message = json.loads(message)
        if message['type'] == 'move':
            self.character.move(DIRECTIONS[message['direction']])
            for c in cl:
                c.write_message(self.get_map_state(c.character))


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    new_map = Map(DEFAULT_OBJECT)
    parse_command_line()
    app.listen(port=PORT)
    tornado.ioloop.IOLoop.instance().start()
