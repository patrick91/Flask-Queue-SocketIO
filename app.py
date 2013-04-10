from collections import deque, namedtuple

from gevent import monkey, sleep; monkey.patch_all()

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from flask import Flask, send_file, request, Request, Response

app = Flask(__name__)

events = deque()

Event = namedtuple('Event', ['type', 'message'])

class QueueNamespace(BaseNamespace):
    def listener(self):
        while True:
            if len(events):
                event = events.pop()

                self.emit('log', event.type, event.message)

            sleep(0.1)

    def on_connect(self):
        self.spawn(self.listener)

@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    socketio_manage(request.environ, {'/log': QueueNamespace}, request)

    return Response()


@app.route('/')
def home():
    return send_file('log.html')


@app.route('/test')
def test():
    events.append(Event('GET', 'Test'))

    return 'test'


if __name__ == "__main__":
    from socketio.server import SocketIOServer

    SocketIOServer(('0.0.0.0', 5000), app,
            resource="socket.io", policy_server=False).serve_forever()
