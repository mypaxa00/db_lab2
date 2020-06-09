class User:
    @staticmethod
    def main_menu():
        print(20 * "^", "Menu", 20 * "^")
        print("3> Exit")
        print("2> Log in")
        print("1> Register")

    @staticmethod
    def user_menu(name):
        print(20 * "^", "User", name, 20 * "^")
        print("4> Log out")
        print("3> Message statistics")
        print("2> Received messages")
        print("1> Send a message")


class Admin:
    @staticmethod
    def admin_menu():
        print(20 * "^", "Admin", 20 * "^")
        print("5> Exit")
        print("4> Show log")
        print("3> Show spamers")
        print("2> Show senders")
        print("1> Show online users")
