import redis
from random import randint
from threading import Thread
from faker import Faker
from src.controller import Controller


class User(Thread):
    def __init__(self, user_connection, username, users_list, users_count, user_controller):
        Thread.__init__(self)
        self.connection = user_connection
        self.users_list = users_list
        self.users_count = users_count
        user_controller.registration(username)
        self.user_id = user_controller.log_in(username, user_connection.hget("users:", username))

    def run(self):
        # infinite loop use [Ctrl] + [C] to stop
        while True:
            message_text = faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
            receiver = users[randint(0, count_users - 1)]
            controller.new_message(message_text, self.user_id, self.connection.hget("users:", receiver))


if __name__ == '__main__':
    faker = Faker()
    # Generating fake users
    users = [faker.profile(fields=['username'], sex=None)['username'] for u in range(10)]
    threads = []
    controller = Controller()
    for x in range(10):
        print(users[x])
        threads.append(
            User(redis.Redis(charset="utf-8", decode_responses=True), users[x], users, 10, controller)
        )
    for t in threads:
        t.start()

    connection = redis.Redis(charset="utf-8", decode_responses=True)
    online = connection.smembers("online:")
    for member in online:
        connection.srem("online:", member)
