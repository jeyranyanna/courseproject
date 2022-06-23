from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.relativelayout import MDRelativeLayout, RelativeLayout
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem, TwoLineListItem
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from Timer import Timer

Window.size = (375, 667)

db = DataBase("users.txt")

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class CreateTask(Screen): # Создание задач
    nameTask = ObjectProperty(None) # Название задачи
    dateTask = ObjectProperty(None) # Дата задачи

    current = ''
    current_user = '' # Получение E-mail того пользователя, чей txt файл мы открываем

    def clear_list(self):
        self.ids.scroll.clear_widgets()

    def view_tasks(self): # Показ задач
        self.ids.scroll.clear_widgets() # Очищаем показ задач
        with open (f'{self.current_user}.txt', 'r') as file: # Открываем файл на чтение
             lines = file.readlines() # Считываем по строкам
             for line in lines:
                 line = line.split(';') # Разделяем на [0] и [1]
                 self.ids.scroll.add_widget(TwoLineListItem(text=f"{line[0]}", secondary_text=f'{line[1]}'))

    def save_task(self): # Сохранение задач в txt файл
        with open(f'{self.current_user}.txt', 'a') as file: # Открываем txt файл
            file.write(self.nameTask.text + ";" + self.dateTask.text + "\n") # Запись (название;дата)

    def error(self): # Всплывающее окно с ошибкой
        pop = Popup(title='Ошибка',
                    content=Label(text='Невозможно создать!'),
                    size_hint=(.8, .3),
                    background_color=[.58, .77, .58, 1],
                    separator_color=[1, 1, 1, 1],
                    title_align='center',
                    title_color=[1, 1, 1, 1])
        pop.open()

    def add_task(self) -> object: # Добавление задачи (проверка)
        if self.nameTask.text != "" and self.dateTask.text != "" and len(self.nameTask.text) <= 15 and len(self.dateTask.text) <= 15:
        # Добавить задание в txt файл + прочитать файл еще раз
            self.save_task()
            self.reset()
        else:
            self.error()

    def reset(self): # Очищение полей ввода
        self.nameTask.text = ""
        self.dateTask.text = ""

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self) -> object:
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0 and len(self.password.text) <= 15:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)
                with open(f'{self.email.text}.txt', 'w') as file: # Создание файла с таким же email
                    print()
                self.reset()

            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    current_user = ''
    current = ''

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            CreateTask.current_user = self.email.text
            self.reset()
            self.manager.current = 'main'
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ''

    def log_out(self):
        Timer.stop_timer(self)
        Timer.is_stopped = True



    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Имя: \n" + name
        self.email.text = "Email: " + self.current
        self.created.text = "Дата регистрации: " + created

    def info(self):
        pop = Popup(title='Техническая поддержка',
                    content=Label(text='E-mail: jeyranyan@bk.ru\nТелефон: 8 (992) 231-49-91'),
                    size_hint=(.8, .3),
                    background_color=[.58, .77, .58, 1],
                    separator_color=[1, 1, 1, 1],
                    title_align='center',
                    title_color=[1, 1, 1, 1])
        pop.open()

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Что-то пошло не так...',
                content=Label(text='Неверный логин или пароль!'),
                size_hint=(.8, .3),
                background_color=[.58, .77, .58, 1],
                separator_color=[1, 1, 1, 1],
                title_align='center',
                title_color=[1, 1, 1, 1])
    pop.open()

def invalidForm() -> object:
    pop = Popup(title='Что-то пошло не так...',
                content=Label(text='Ошибка ввода!'),
                size_hint=(.8, .3),
                background_color=[.58, .77, .58, 1],
                separator_color=[1, 1, 1, 1],
                title_align='center',
                title_color=[1, 1, 1, 1],)
    pop.open()

class Navbar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass

class MyMainApp(MDApp):


    def build(self):
        Builder.load_file('timer.kv')
        return Builder.load_file('my.kv')

if __name__ == '__main__':
    MyMainApp().run()