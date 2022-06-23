import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def alreadyReg(self):
        pop = Popup(title='Ошибка',
                    content=Label(text='Такой E-mail уже используется!\n'
                                       'Используйте другой или \nвойдите в аккаунт'),
                    size_hint=(.8, .3),
                    background_color=[.58, .77, .58, 1],
                    separator_color=[1, 1, 1, 1],
                    title_align='center',
                    title_color=[1, 1, 1, 1])
        pop.open()

    def agreeReg(self):
        pop = Popup(title='Успешно!',
                    content=Label(text='Аккаунт создан!'),
                    size_hint=(.8, .3),
                    background_color=[.58, .77, .58, 1],
                    separator_color=[1, 1, 1, 1],
                    title_align='center',
                    title_color=[1, 1, 1, 1])
        pop.open()

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            print(self.users[email.strip()])
            self.save()
            self.agreeReg()
            return 1
        else:
            self.alreadyReg()
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]