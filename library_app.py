from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
# Config.set('graphics', 'width', '360')
# Config.set('graphics', 'height', '640')
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingIcon, \
    MDListItemLeadingIcon, MDListItem, MDListItemHeadlineText
from KivyMD.kivymd.uix.dialog import MDDialogHeadlineText
from kivy.properties import StringProperty
import sqlite3
from library_books import books_by_category
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogSupportingText
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
import random


# --- Database Setup ---
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Librarians (
    librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT UNIQUE NOT NULL
)
""")
# Insert default librarian credentials
try:
    cursor.execute("""
    INSERT INTO Librarians (name, password)
    VALUES (?, ?)
    ON CONFLICT(password) DO NOTHING
    """, ('Librarian Name', 'librarian'))
    conn.commit()
except sqlite3.IntegrityError:
    pass

conn.close()





# --- Database Setup ---
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        student_number TEXT UNIQUE NOT NULL
    )
''')
conn.commit()
conn.close()

# --- Database Setup ---
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        category TEXT,
        availability TEXT
    )
''')
conn.commit()
conn.close()

# --- Your Components ---
class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class BaseScreen(MDScreen):
    pass
    #image_size = StringProperty()

class ProfileScreen(MDScreen):
    pass

class LibrarianDashboardScreen(MDScreen):
    pass
class ViewBorrowedLibrarianScreen(MDScreen):
    pass
class PenaltyLibrarianScreen(MDScreen):
    pass
class BorrowRequestScreen(MDScreen):
    pass

class ReturnRequestScreen(MDScreen):
    pass

class InformationTechnologyScreen(MDScreen):
    pass

class HospitalityManagementScreen(MDScreen):
    pass

class ComputerEngineeringScreen(MDScreen):
    pass

class OfficeAdministrationScreen(MDScreen):
    pass

class PhysicalEducationScreen(MDScreen):
    pass

class ViewBooksScreen(MDScreen):
    pass

class RegisterBooksScreen(MDScreen):
    dialog = None
    def register_book(self, title, author, category, availability):
        if not title or not author or not category or not availability:
            self.show_dialog("Please fill all fields.")
            return

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO books (title, author, category, availability)
            VALUES (?, ?, ?, ?)
        ''', (title, author, category, availability))

        conn.commit()
        conn.close()

        self.show_dialog(f"Book '{title}' registered successfully!")

        # Optional: Clear fields after registering
        self.ids.register_book_title.text = ""
        self.ids.register_book_author.text = ""
        self.ids.register_book_category.text = ""
        self.ids.register_book_availability.text = ""

        # Optional: Go to view books screen automatically
        #self.manager.current = "view_books_screen"

    def show_dialog(self, text):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            MDDialogSupportingText(
                text=text,
                halign="left",
                size_hint_x=1,
            ),
                MDDialogHeadlineText(
                    text= "",
                    halign = "left",
                ),

                MDButton(
                    MDButtonText(text="OK",),
                    on_press=lambda x: self.dialog.dismiss(),
                )

            )

        self.dialog.open()

class ViewBorrowedScreen(MDScreen):
    pass

class ReturnBooksScreen(MDScreen):
    pass

class PenaltyScreen(MDScreen):
    pass

class LibrarianScreen(MDScreen):
    dialog = None

    def login_librarian(self, librarian_name, librarian_password):
        if not librarian_name.strip() or not librarian_password.strip():
            self.show_dialog("Please enter name and password.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Librarians WHERE name = ? AND password= ?", (librarian_name, librarian_password))
        existing = cursor.fetchone()
        conn.close()

        if existing:
            self.show_dialog(f"Welcome to Library App, {librarian_name}!")
            #MDApp.get_running_app().logged_in_student_number = existing[3]
            MDApp.get_running_app().root.current = "librarian_dashboard_screen"

            # Optional: Clear fields after registering
            self.ids.librarian_name.text = ""
            self.ids.librarian_password.text = ""

        else:
            self.show_dialog("No matching account found.")

    def show_dialog(self, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    on_release=lambda x: self.dialog.dismiss()
                )
            )
        )
        self.dialog.open()

# --- Login and Register Screens ---
class LoginScreen(MDScreen):
    dialog = None

    def login_student(self, name, student_number):
        if not name.strip() or not student_number.strip():
            self.show_dialog("Please enter name and student number.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ? AND student_number = ?", (name, student_number))
        existing = cursor.fetchone()
        conn.close()

        if existing:
            # Save logged in student globally
            self.show_dialog(f"Welcome to Library App, {name}!")
            MDApp.get_running_app().logged_in_student_number = existing[3]
            MDApp.get_running_app().root.current = "main_screen"

            # Optional: Clear fields after registering
            self.ids.name.text = ""
            self.ids.student_number.text = ""

        else:
            self.show_dialog("No matching account found.")

    def show_dialog(self, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    on_release=lambda x: self.dialog.dismiss()
                )
            )
        )
        self.dialog.open()


class RegisterScreen(MDScreen):
    dialog = None

    def register_student(self, name, email, student_number):
        if not name or not email or not student_number:
            self.show_dialog("Please fill in all fields.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Check for duplicates
        cursor.execute("SELECT * FROM users WHERE email = ? OR student_number = ?",
                       (email, student_number))
        existing = cursor.fetchone()

        if existing:
            conn.close()
            self.show_dialog("Email or Student Number already used. Try different values.")
            return

        cursor.execute("INSERT INTO users (name, email, student_number) VALUES (?, ?, ?)",
                       (name, email, student_number))
        conn.commit()
        conn.close()

        self.show_dialog(f"Student '{name}' registered successfully!")

        # Clear fields
        self.ids.register_name.text = ""
        self.ids.register_email.text = ""
        self.ids.register_student_number.text = ""

    def show_dialog(self, text):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    on_release=lambda x: self.dialog.dismiss()
                )
            )
        )
        self.dialog.open()

# --- Main App ---
class AnoWalangTutulong(MDApp):
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


    def switch_screen(self, screen_name):
        self.root.current = screen_name


    # Home screen book recommendations
    # def load_recommended_books(self):
    #     main_screen = self.root.get_screen("main_screen")
    #     home_screen = main_screen.ids.screen_manager.get_screen("home_screen")
    #     container = home_screen.ids.home_recommendations_list
    #     container.clear_widgets()
    #
    #     try:
    #         # Access 'main_screen'
    #         main_screen = self.root.get_screen("main_screen")
    #
    #         # Access the inner screen_manager
    #         screen_manager = main_screen.ids.get("screen_manager")
    #         if not screen_manager:
    #             print("⚠️ screen_manager not found in ids")
    #             return
    #
    #         # Access 'home_screen' inside screen_manager
    #         home_screen = screen_manager.get_screen("home_screen")
    #         container = home_screen.ids.get("home_recommendations_list")
    #
    #         if container:
    #             container.clear_widgets()
    #             # recommended book widgets
    #             conn = sqlite3.connect("library.db")
    #             cursor = conn.cursor()
    #
    #             # Get distinct categories
    #             cursor.execute("SELECT DISTINCT category FROM books")
    #             categories = cursor.fetchall()
    #
    #             for cat in categories:
    #                 category = cat[0]
    #
    #                 # Add category label
    #                 container.add_widget(MDLabel(
    #                     text=f"[b]{category} (Top 3)[/b]",
    #                     markup=True,
    #                     #font_style="H6",
    #                     size_hint_y=None,
    #                     height="40dp"
    #                 ))
    #
    #                 # Fetch 3 random books from this category
    #                 cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?", (category,))
    #                 all_books = cursor.fetchall()
    #
    #                 selected_books = random.sample(all_books, min(3, len(all_books)))
    #
    #                 for book_id, title, author, availability in selected_books:
    #                     item = MDListItem()
    #
    #                     item.add_widget(MDListItemLeadingIcon(icon="book"))
    #                     item.add_widget(MDListItemHeadlineText(text=f"{title} | {book_id}"))
    #                     item.add_widget(MDListItemSupportingText(text=author))
    #                     item.add_widget(MDListItemTertiaryText(text=f"{availability}"))
    #
    #                     # Optional: Add action buttons
    #                     item.add_widget(MDListItemTrailingIcon(icon="heart-outline"))
    #                     item.add_widget(MDListItemTrailingIcon(icon="book-clock"))
    #
    #                     container.add_widget(item)
    #
    #             conn.close()
    #         else:
    #             print("⚠️ home_recommendations_list not found")
    #
    #     except Exception as e:
    #         print(f"❌ Error loading recommendations: {e}")




    # For Librarian Screen icon button
    def toggle_librarian_password_visibility(self):
        screen = self.root.get_screen('librarian_screen')
        password_field = screen.ids.librarian_password
        icon = screen.ids.password_icon

        password_field.password = not password_field.password
        icon.icon = "eye" if not password_field.password else "eye-off"


    # For Information Technology Screen
    def load_information_technology_books(self):
        screen = self.root.get_screen('information_technology_screen')
        container = screen.ids.it_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?",
                       ("Information Technology",))
        books = cursor.fetchall()
        conn.close()

        from kivymd.uix.list import (
            MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText,
            MDListItemSupportingText, MDListItemTertiaryText
        )
        from kivymd.uix.card import MDCard

        for book in books:
            book_id, title, author, availability = book

            it_item = MDListItem()
            #it_item.theme_bg_color= 'Custom'
            #it_item.md_bg_color = (0.2, 0.4, 1, 0.15) # Light blue background

            it_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            it_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            it_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            it_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",  # adjust spacing of icons
                spacing="5dp"
            )

            # # Delete Button
            # delete_button = MDIconButton(
            #     icon="trash-can-outline",
            #     theme_icon_color="Custom",
            #     icon_color=(1, 0, 0, 1),
            #     on_release=lambda x, bid=book_id: self.delete_book(bid)
            # )
            # trailing_buttons.add_widget(delete_button)

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.favorite_book(bid)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button)

            # Add trailing_buttons to MDListItem (RIGHT SIDE EFFECT)
            it_item.add_widget(trailing_buttons)

            container.add_widget(it_item)


    # For Hospitality Management Screen
    def load_hospitality_management_books(self):
        screen = self.root.get_screen('hospitality_management_screen')
        container = screen.ids.hm_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?",
                       ("Hospitality Management",))
        books = cursor.fetchall()
        conn.close()



        for book in books:
            book_id, title, author, availability = book

            hm_item = MDListItem()
            #hm_item.theme_bg_color = 'Custom'
            hm_item.md_bg_color = (0.2, 0.4, 1, 0.15)

            hm_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            hm_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            hm_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            hm_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",  # adjust spacing of icons
                spacing="5dp"
            )

            # # Delete Button
            # delete_button = MDIconButton(
            #     icon="trash-can-outline",
            #     theme_icon_color="Custom",
            #     icon_color=(1, 0, 0, 1),
            #     on_release=lambda x, bid=book_id: self.delete_book(bid)
            # )
            # trailing_buttons.add_widget(delete_button)

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.favorite_book(bid)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button)

            # Add trailing_buttons to MDListItem (RIGHT SIDE EFFECT)
            hm_item.add_widget(trailing_buttons)

            container.add_widget(hm_item)

    # For Computer Engineering Screen
    def load_computer_engineering_books(self):
        screen = self.root.get_screen('computer_engineering_screen')
        container = screen.ids.cpe_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?",
                       ("Computer Engineering",))
        books = cursor.fetchall()
        conn.close()


        for book in books:
            book_id, title, author, availability = book

            cpe_item = MDListItem()
            #cpe_item.theme_bg_color = 'Custom'
            cpe_item.md_bg_color = (0.2, 0.4, 1, 0.15)  # Light blue background


            cpe_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            cpe_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            cpe_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            cpe_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",  # adjust spacing of icons
                spacing="5dp"
            )

            # # Delete Button
            # delete_button = MDIconButton(
            #     icon="trash-can-outline",
            #     theme_icon_color="Custom",
            #     icon_color=(1, 0, 0, 1),
            #     on_release=lambda x, bid=book_id: self.delete_book(bid)
            # )
            # trailing_buttons.add_widget(delete_button)

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.favorite_book(bid)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button)

            # Add trailing_buttons to MDListItem (RIGHT SIDE EFFECT)
            cpe_item.add_widget(trailing_buttons)

            container.add_widget(cpe_item)

    # For Office Administration Screen
    def load_office_administration_books(self):
        screen = self.root.get_screen('office_administration_screen')
        container = screen.ids.oa_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?",
                       ("Office Administration",))
        books = cursor.fetchall()
        conn.close()


        for book in books:
            book_id, title, author, availability = book

            oa_item = MDListItem()
            #oa_item.theme_bg_color = 'Custom'
            oa_item.md_bg_color = (0.2, 0.4, 1, 0.15)

            oa_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            oa_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            oa_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            oa_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",  # adjust spacing of icons
                spacing="5dp"
            )

            # # Delete Button
            # delete_button = MDIconButton(
            #     icon="trash-can-outline",
            #     theme_icon_color="Custom",
            #     icon_color=(1, 0, 0, 1),
            #     on_release=lambda x, bid=book_id: self.delete_book(bid)
            # )
            # trailing_buttons.add_widget(delete_button)

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.favorite_book(bid)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button)

            # Add trailing_buttons to MDListItem (RIGHT SIDE EFFECT)
            oa_item.add_widget(trailing_buttons)

            container.add_widget(oa_item)

    # Physical Education Screen
    def load_physical_education_books(self):
        screen = self.root.get_screen('physical_education_screen')
        container = screen.ids.pe_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?",
                       ("PE",))
        books = cursor.fetchall()
        conn.close()


        for book in books:
            book_id, title, author, availability = book

            pe_item = MDListItem()
            #pe_item.theme_bg_color = 'Custom'
            pe_item.md_bg_color = (0.2, 0.4, 1, 0.15)

            pe_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            pe_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            pe_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            pe_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",  # adjust spacing of icons
                spacing="5dp"
            )

            # # Delete Button
            # delete_button = MDIconButton(
            #     icon="trash-can-outline",
            #     theme_icon_color="Custom",
            #     icon_color=(1, 0, 0, 1),
            #     on_release=lambda x, bid=book_id: self.delete_book(bid)
            # )
            # trailing_buttons.add_widget(delete_button)

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.favorite_book(bid)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button)

            # Add trailing_buttons to MDListItem (RIGHT SIDE EFFECT)
            pe_item.add_widget(trailing_buttons)

            container.add_widget(pe_item)



    # For View Books Screen
    def load_books(self):
        screen = self.root.get_screen('view_books_screen')
        container = screen.ids.table_container
        container.clear_widgets()

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, category, availability FROM books")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            book_id, title, author, category, availability = row

            list_item = MDListItem()


            list_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))

            list_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            list_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            list_item.add_widget(MDListItemTertiaryText(text=f"Category:  {category}     |     Availability:  {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",  # adjust spacing of icons
                spacing="5dp"
            )

            # Delete Button
            delete_button = MDIconButton(
                icon="trash-can-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0, 1),
                on_release=lambda x, bid=book_id: self.delete_book(bid)
            )
            trailing_buttons.add_widget(delete_button)
            #
            # # Favorite Button
            # favorite_button = MDIconButton(
            #     icon="heart-outline",
            #     theme_icon_color="Custom",
            #     icon_color=(1, 0, 0.5, 1),
            #     on_release=lambda x, bid=book_id: self.favorite_book(bid)
            # )
            # trailing_buttons.add_widget(favorite_button)
            #
            # # Borrow Button
            # borrow_button = MDIconButton(
            #     icon="book-open-page-variant",
            #     theme_icon_color="Custom",
            #     icon_color=(0, 0.5, 1, 1),
            #     on_release=lambda x, bid=book_id: self.borrow_book(bid)
            # )
            # trailing_buttons.add_widget(borrow_button)
            #
            # # Add trailing_buttons to MDListItem (RIGHT SIDE EFFECT)
            list_item.add_widget(trailing_buttons)

            container.add_widget(list_item)

    def insert_books_from_data(self):
        # Insert database
        conn = sqlite3.connect("library.db")
        c = conn.cursor()

        for category, books in books_by_category.items():
            for book in books:
                # Check if book already exists in the database (ignoring availability)
                c.execute("SELECT * FROM books WHERE title = ? AND author = ? AND category = ?",
                          (book['title'], book['author'], category))
                existing_book = c.fetchone()
                if existing_book is None:
                    c.execute("""INSERT INTO books (title, author,category, availability)
                            VALUES (?, ?, ?, ?)""",
                              (book['title'], book['author'], category, book['availability']))

        conn.commit()
        conn.close()

    def delete_book(self, book_id):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()

        # Refresh table
        self.load_books()

    def favorite_book(self, book_id):
        print(f"Marked book {book_id} as favorite.")

    def borrow_book(self, book_id):
        print(f"Borrowed book {book_id}.")

    #dito burahin


    def build(self):
        self.insert_books_from_data()
        return Builder.load_file("library_app.kv")

if __name__ == "__main__":
    AnoWalangTutulong().run()
