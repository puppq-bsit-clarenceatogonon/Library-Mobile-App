from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
from kivymd.uix.screenmanager import MDScreenManager


from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen



class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

# class ScreenManager(MDScreenManager):
#     pass

class BaseScreen(MDScreen):
    image_size = StringProperty()

# class LoginScreen(MDScreen):
#     pass
#
# class RegisterScreen(MDScreen):
#     pass



class Example(MDApp):
    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        screen_map = {
            "Home": "home_screen",
            "Favorites": "favorites_screen",
            "Search": "search_screen",
            "Categories": "categories_screen"
        }

        target_screen = screen_map.get(item_text)
        if target_screen:
            self.root.ids.screen_manager.current = target_screen

    def build(self):
        return Builder.load_file("main_to_tangina.kv")


if __name__ == "__main__":
    Example().run()
