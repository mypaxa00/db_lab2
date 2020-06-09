import logging
from threading import Thread

logging.basicConfig(filename="events.log", level=logging.INFO)


class ConnectionListener(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        subscribe = self.connection.pubsub()
        subscribe.subscribe(["users", "spam"])

        for item in subscribe.listen():
            if item['type'] == 'message':
                logging.info(item['data'])
