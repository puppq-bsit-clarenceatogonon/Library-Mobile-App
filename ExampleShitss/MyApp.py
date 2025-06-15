from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import NoTransition

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager



class LogScreen(MDScreen):
    pass

class HomeScreen(MDScreen):
    pass

class FavoritesScreen(MDScreen):
    pass

class SearchScreen(MDScreen):
    pass

class CategoriesScreen(MDScreen):
    pass

class WindowManager(MDScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        sm = Builder.load_file("my.kv")
        sm.transition = NoTransition()
        return sm

    def switch_screen(self, screen_name):
        self.root.current = screen_name







if __name__== "__main__":
    MyApp().run()