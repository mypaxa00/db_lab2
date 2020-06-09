import logging
from src.controller import Controller


logging.basicConfig(filename="events.log", level=logging.INFO)


def main():
    controller = Controller()
    controller.start_admin()


if __name__ == '__main__':
    main()
