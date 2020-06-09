import random
import datetime
import time
from threading import Thread
import redis


class MessageWorker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.connection = redis.Redis(charset="utf-8", decode_responses=True)
        self.delay = random.randint(0, 3)

    def run(self):
        while True:
            message = self.connection.brpop("in_queue:")

            if message:
                message_id = int(message[1])

                self.connection.hmset('message:%s' % message_id, {
                    'status': 'need_to_check'
                })

                message = self.connection.hmget("message:%s" % message_id, ["message_sender_id", "message_consumer_id"])
                sender_id = int(message[0])

                self.connection.hincrby("user:%s" % sender_id, "in_queue", -1)
                self.connection.hincrby("user:%s" % sender_id, "need_to_check", 1)

                time.sleep(self.delay)
                is_spam = random.random() > 0.5

                pipeline = self.connection.pipeline(True)
                pipeline.hincrby("user:%s" % sender_id, "need_to_check", -1)

                if is_spam:
                    sender_username = self.connection.hmget("user:%s" % sender_id, ["username"])[0]

                    pipeline.zincrby("spam:", 1, "user:%s" % sender_username)
                    pipeline.hmset('message:%s' % message_id, {
                        'status': 'blocked_for_spam'
                    })
                    pipeline.hincrby("user:%s" % sender_id, "blocked_for_spam", 1)
                    pipeline.publish('spam', f"{datetime.datetime.now()}: Spam check: user \"%s\" sent spam message: "
                                             f"\"%s\"\n" % (sender_username,
                                        self.connection.hmget("message:%s" % message_id, ["message_text"])[0]))

                else:
                    pipeline.hmset('message:%s' % message_id, {
                        'status': 'sent_to_user'
                    })
                    pipeline.hincrby("user:%s" % sender_id, "sent_to_user", 1)
                    pipeline.sadd("sentto:%s" % int(message[1]), message_id)

                pipeline.execute()


def main():
    for x in range(5):
        worker = MessageWorker()
        worker.daemon = True
        worker.start()
    while True:
        pass


if __name__ == '__main__':
    main()