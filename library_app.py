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
from datetime import datetime


conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS borrowed_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    student_number TEXT,
    book_id INTEGER,
    book_title TEXT,
    book_author TEXT,
    category TEXT,
    date_borrowed TEXT,
    date_returned TEXT,
    return_status TEXT DEFAULT 'Not Returned'
)
""")

conn.commit()
conn.close()

conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS return_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    student_number TEXT,
    book_id INTEGER, 
    book_title TEXT,
    author TEXT,
    category TEXT,
    status TEXT DEFAULT 'Pending',
    date_requested TEXT,
    date_approved TEXT
)
""")
conn.commit()
conn.close()

# --- Create BorrowRequests Table ---
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS borrow_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT,
    student_name TEXT,
    book_id INTEGER,
    book_title TEXT,
    book_author TEXT,
    category TEXT,
    status TEXT DEFAULT 'Pending',
    date_requested TEXT,
    date_approved TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT,
    book_id INTEGER,
    title TEXT,
    author TEXT,
    category TEXT
)
""")

conn.commit()
conn.close()


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

class HomeScreen(MDScreen):
    pass


class FavoritesScreen(MDScreen):
    pass

class SearchScreen(MDScreen):
    pass

class CategoriesScreen(MDScreen):
    pass

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
    def load_recommended_books(self):

        home_screen = self.root.get_screen("home_screen")
        container = home_screen.ids.home_recommendations_list
        container.clear_widgets()

        try:

            if container:
                container.clear_widgets()
                # recommended book widgets
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()

                # Get distinct categories
                cursor.execute("SELECT DISTINCT category FROM books")
                categories = cursor.fetchall()

                for cat in categories:
                    category = cat[0]

                    # Add category label
                    container.add_widget(MDLabel(
                        text=f"[b]{category} (Top 3)[/b]",
                        markup=True,
                        #font_style="H6",
                        size_hint_y=None,
                        height="40dp"
                    ))

                    # Fetch 3 random books from this category
                    cursor.execute("SELECT id, title, author, availability FROM books WHERE category = ?", (category,))
                    all_books = cursor.fetchall()

                    selected_books = random.sample(all_books, min(3, len(all_books)))

                    for book_id, title, author, availability in selected_books:
                        item = MDListItem()

                        item.add_widget(MDListItemLeadingIcon(icon="book"))
                        item.add_widget(MDListItemHeadlineText(text=f"{title} | {book_id}"))
                        item.add_widget(MDListItemSupportingText(text=author))
                        item.add_widget(MDListItemTertiaryText(text=f"{availability}"))

                        # Optional: Add action buttons
                        item.add_widget(MDListItemTrailingIcon(icon="heart-outline"))
                        item.add_widget(MDListItemTrailingIcon(icon="book-clock"))

                        container.add_widget(item)

                conn.close()
            else:
                print(" home_recommendations_list not found")

        except Exception as e:
            print(f" Error loading recommendations: {e}")




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
        cursor.execute("SELECT id, title, author, category, availability FROM books WHERE category = ?",
                       ("Information Technology",))
        books = cursor.fetchall()
        conn.close()

        from kivymd.uix.list import (
            MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText,
            MDListItemSupportingText, MDListItemTertiaryText
        )
        from kivymd.uix.card import MDCard

        for book in books:
            book_id, title, author, category, availability = book

            it_item = MDListItem()
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


            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.add_to_favorites(bid, title, author, category)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button_request = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button_request)
            if availability.lower() != "available":
                borrow_button_request.disabled = True

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
        cursor.execute("SELECT id, title, author, category, availability FROM books WHERE category = ?",
                       ("Hospitality Management",))
        books = cursor.fetchall()
        conn.close()



        for book in books:
            book_id, title, author, category, availability = book

            hm_item = MDListItem()
            hm_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            hm_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            hm_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            hm_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container (RIGHT SIDE)
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",
                spacing="5dp"
            )



            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.add_to_favorites(bid, title, author, category)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button_request = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            trailing_buttons.add_widget(borrow_button_request)
            if availability.lower() != "available":
                borrow_button_request.disabled = True

            # Add trailing_buttons to MDListItem
            hm_item.add_widget(trailing_buttons)

            container.add_widget(hm_item)

    # For Computer Engineering Screen
    def load_computer_engineering_books(self):
        screen = self.root.get_screen('computer_engineering_screen')
        container = screen.ids.cpe_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, category, availability FROM books WHERE category = ?",
                       ("Computer Engineering",))
        books = cursor.fetchall()
        conn.close()


        for book in books:
            book_id, title, author, category, availability = book

            cpe_item = MDListItem()
            cpe_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            cpe_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            cpe_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            cpe_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",
                spacing="5dp"
            )

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.add_to_favorites(bid, title, author, category)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button_request = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            if availability.lower() != "available":
                borrow_button_request.disabled = True

            trailing_buttons.add_widget(borrow_button_request)

            # Add trailing_buttons to MDListItem
            cpe_item.add_widget(trailing_buttons)

            container.add_widget(cpe_item)

    # For Office Administration Screen
    def load_office_administration_books(self):
        screen = self.root.get_screen('office_administration_screen')
        container = screen.ids.oa_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, category, availability FROM books WHERE category = ?",
                       ("Office Administration",))
        books = cursor.fetchall()
        conn.close()


        for book in books:
            book_id, title, author, category, availability = book

            oa_item = MDListItem()
            oa_item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            oa_item.add_widget(MDListItemHeadlineText(text=f"Title:  {title} | Book ID: {book_id}"))
            oa_item.add_widget(MDListItemSupportingText(text=f"Author:  {author}"))
            oa_item.add_widget(MDListItemTertiaryText(text=f"Availability: {availability}"))

            # Trailing Buttons Container
            trailing_buttons = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=None,
                width="120dp",
                spacing="5dp"
            )

            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.add_to_favorites(bid, title, author, category)
            )
            trailing_buttons.add_widget(favorite_button)

            # Borrow Button
            borrow_button_request = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )
            if availability.lower() != "available":
                borrow_button_request.disabled = True

            trailing_buttons.add_widget(borrow_button_request)

            # Add trailing_buttons to MDListItem
            oa_item.add_widget(trailing_buttons)

            container.add_widget(oa_item)

    # Physical Education Screen
    def load_physical_education_books(self):
        screen = self.root.get_screen('physical_education_screen')
        container = screen.ids.pe_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author,category, availability  FROM books WHERE category = ?",
                       ("PE",))
        books = cursor.fetchall()
        conn.close()


        for book in books:
            book_id, title, author, category, availability = book

            pe_item = MDListItem()
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


            # Favorite Button
            favorite_button = MDIconButton(
                icon="heart-outline",
                theme_icon_color="Custom",
                icon_color=(1, 0, 0.5, 1),
                on_release=lambda x, bid=book_id: self.add_to_favorites(bid, title, author, category)
            )
            trailing_buttons.add_widget(favorite_button)



            # Borrow Button
            borrow_button_request = MDIconButton(
                icon="book-open-page-variant",
                theme_icon_color="Custom",
                icon_color=(0, 0.5, 1, 1),
                on_release=lambda x, bid=book_id: self.borrow_book(bid)
            )

            if availability.lower() != "available":
                borrow_button_request.disabled = True

            trailing_buttons.add_widget(borrow_button_request)

            # Add trailing_buttons to MDListItem
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

            # # Add trailing_buttons to MDListItem
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

    def add_to_favorites(self, book_id, title, author, category):
        student_number = getattr(self, 'logged_in_student_number', None)
        if not student_number:
            self.show_generic_dialog("Login required to add favorites.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM favorites
            WHERE student_number = ? AND book_id = ?
        """, (student_number, book_id))

        if cursor.fetchone():
            self.show_generic_dialog("Already in favorites.")
        else:
            cursor.execute("""
                INSERT INTO favorites (student_number, book_id, title, author, category)
                VALUES (?, ?, ?, ?, ?)
            """, (student_number, book_id, title, author, category))
            conn.commit()
            self.show_generic_dialog("Added to favorites!")

        conn.close()

    # --- Load Favorites ---
    def load_favorites(self):
        try:
            favorites_screen = self.root.get_screen("favorites_screen")
            container = favorites_screen.ids.favorites_container
            container.clear_widgets()

            student_number = getattr(self, "logged_in_student_number", None)
            print(" Logged in student number:", student_number)

            if not student_number:
                self.show_generic_dialog("Please log in first.")
                return

            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT book_id, title, author, category 
                FROM favorites 
                WHERE student_number = ?
            """, (student_number,))
            favorites = cursor.fetchall()
            conn.close()

            for book_id, title, author, category in favorites:
                print(f" Adding favorite: {title} | {book_id}")
                item = MDListItem(size_hint_y=None, height="100dp")
                item.add_widget(MDListItemLeadingIcon(icon="book"))
                item.add_widget(MDListItemHeadlineText(text=f"{title} | ID: {book_id}"))
                item.add_widget(MDListItemSupportingText(text=f"Author: {author}"))
                item.add_widget(MDListItemTertiaryText(text=f"Category: {category}"))

                container.add_widget(item)

        except Exception as e:
            print(f" Error loading favorites: {e}")

    # here

    def request_return_book(self, book_id, title, author, category):
        student_number = getattr(self, 'logged_in_student_number', None)
        if not student_number:
            self.show_generic_dialog("Login required to return books.")
            return

        # Get student name
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE student_number = ?", (student_number,))
        student = cursor.fetchone()

        if not student:
            conn.close()
            self.show_generic_dialog("Student not found.")
            return

        student_name = student[0]
        date_requested = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

        #  Check for existing pending return request
        cursor.execute("""
            SELECT * FROM return_requests
            WHERE student_number = ? AND book_id = ? AND book_title = ? AND author = ? AND category = ? AND status = 'Pending'
        """, (student_number, book_id, title, author, category))
        existing_request = cursor.fetchone()

        if existing_request:
            conn.close()
            self.show_generic_dialog("You already have a pending return request for this book.")
            return

        # Proceed to insert if no duplicate
        cursor.execute("""
            INSERT INTO return_requests (student_number, student_name, book_id, book_title, author, category, date_requested, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
        """, (student_number, student_name, book_id, title, author, category, date_requested))
        conn.commit()
        conn.close()

        self.show_generic_dialog("Return request submitted!")

    def load_return_requests(self):
        screen = self.root.get_screen("return_request_screen")
        container = screen.ids.return_requests_container
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, student_name, student_number, book_id, book_title, author, category, status, date_requested, date_approved FROM return_requests")

        requests = cursor.fetchall()
        conn.close()

        for req in requests:
            request_id, name, student_no, book_id, book_title, author,category, status, date_requested, date_approved  = req

            list_item = MDListItem()
            list_item.add_widget(MDListItemLeadingIcon(icon="account"))
            list_item.add_widget(MDListItemHeadlineText(text=f"{name} | {student_no}"))
            list_item.add_widget(MDListItemSupportingText(text=f"{book_title} by {author} | {category}"))
            list_item.add_widget(MDListItemTertiaryText(text=f"Requested: {date_requested}  |  Status: {status}  |  Date approved: {date_approved}"))

            if status == "Pending":
                trailing_buttons = MDBoxLayout(
                    orientation="horizontal",
                    size_hint_x=None,
                    width="120dp",  # adjust spacing of icons
                    spacing="5dp"
                )


                # APPROVE BUTTON
                approve_btn = MDIconButton(
                    icon="check",
                    theme_icon_color="Custom",
                    icon_color=(0, 0.8, 0, 1),
                    on_release=lambda x, rid=request_id: self.update_return_status(rid, "Approved")
                )
                trailing_buttons.add_widget(approve_btn)

                # REJECT BUTTON
                reject_btn = MDIconButton(
                    icon="close",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    on_release=lambda x, rid=request_id: self.update_return_status(rid, "Rejected")
                )
                trailing_buttons.add_widget(reject_btn)

                list_item.add_widget(trailing_buttons)

            container.add_widget(list_item)
            #container.add_widget(approve_btn)
            #container.add_widget(reject_btn)

    def update_return_status(self, request_id, new_status):
        date_approved = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Get book and student info
        cursor.execute("SELECT book_id, book_title, author, category, student_number FROM return_requests WHERE id = ?", (request_id,))
        book_data = cursor.fetchone()

        if book_data:
            book_id, book_title, book_author, category, student_number = book_data

            if new_status == "Approved":
                #  Set book as available again
                cursor.execute("""
                    UPDATE books
                    SET availability = 'Available'
                    WHERE id = ? AND title = ? AND author = ? AND category = ?
                """, (book_id, book_title, book_author, category))

                #  Update borrowed_books with return date and status
                cursor.execute("""
                    UPDATE borrowed_books
                    SET date_returned = ?, return_status = 'Returned'
                    WHERE student_number = ? AND book_title = ? AND book_author = ?
                """, (date_approved, student_number, book_title, book_author))

        #  Update return_requests table
        cursor.execute("""
            UPDATE return_requests 
            SET status = ?, date_approved = ?
            WHERE id = ?
        """, (new_status, date_approved, request_id))

        conn.commit()
        conn.close()
        self.load_return_requests()


    # refresh the list

    def borrow_book(self, book_id):
        # Get book info
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, category FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        conn.close()

        if not book:
            return

        book_id, title, author, category = book

        # Get logged-in student
        student_number = getattr(self, 'logged_in_student_number', None)
        if not student_number:
            self.show_generic_dialog("Login required to borrow books.")
            return

        # Fetch student name
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE student_number = ?", (student_number,))
        student = cursor.fetchone()
        conn.close()

        if not student:
            self.show_generic_dialog("Student not found.")
            return

        student_name = student[0]

        # Show confirmation dialog
        def confirm_borrow(*args):
            date_requested = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")

            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()

            # Check for existing borrow request
            cursor.execute("""
                SELECT * FROM borrow_requests
                WHERE student_number = ? AND book_id = ? AND book_title = ? AND book_author = ? AND category = ? AND status = 'Pending'
            """, (student_number,book_id, title, author, category))
            existing_request = cursor.fetchone()

            if existing_request:
                self.dialog.dismiss()
                self.show_generic_dialog("You already have a pending borrow request for this book.")
                conn.close()
                return

            # Proceed if no duplicate
            cursor.execute("""
                INSERT INTO borrow_requests (
                    student_number, 
                    student_name, 
                    book_id,
                    book_title, 
                    book_author, 
                    category,
                    date_requested
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (student_number, student_name, book_id, title, author,category, date_requested))
            conn.commit()
            conn.close()
            self.dialog.dismiss()
            self.show_generic_dialog("Your borrow request has been sent.")

        self.dialog = MDDialog(
            MDDialogSupportingText(text=f"Are you sure you want to borrow:\n\nTitle: {title}\nAuthor: {author}"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Cancel"), on_release=lambda x: self.dialog.dismiss()),
                MDButton(MDButtonText(text="Yes"), on_release=confirm_borrow)
            )
        )
        self.dialog.open()

    def show_generic_dialog(self, message):
        if hasattr(self, 'info_dialog') and self.info_dialog:
            self.info_dialog.dismiss()

        self.info_dialog = MDDialog(
            MDDialogSupportingText(text=message),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="OK"), on_release=lambda x: self.info_dialog.dismiss())
            )
        )
        self.info_dialog.open()

    def load_borrow_requests(self):
        screen = self.root.get_screen("borrow_request_screen")
        container = screen.ids.borrow_requests_container
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            """SELECT rowid,
                    student_name,
                    student_number, 
                    book_id,
                    book_title,
                    book_author,
                    category,
                    status,
                    date_requested,
                    date_approved FROM borrow_requests""")
        requests = cursor.fetchall()
        conn.close()

        for request in requests:
            rowid, student_name, student_number, book_id, book_title, book_author, category, status, date_requested, date_approved = request

            item = MDListItem()
            item.add_widget(MDListItemLeadingIcon(icon="account"))
            item.add_widget(MDListItemHeadlineText(text=f"{student_name} | {student_number}"))
            item.add_widget(MDListItemSupportingText(text=f"{book_title} by {book_author}  |  {category}"))
            item.add_widget(MDListItemTertiaryText(text=f"Requested: {date_requested}  |  Status: {status}  |  Date approved: {date_approved}"))

            # Only show buttons if not yet approved/rejected
            if status == "Pending":
                accept_btn = MDIconButton(
                    icon="check",
                    theme_icon_color="Custom",
                    icon_color=(0, 0.8, 0, 1),
                    on_release=lambda x, r=rowid: self.update_borrow_status(r, "Approved")
                )
                reject_btn = MDIconButton(
                    icon="close",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    on_release=lambda x, r=rowid: self.update_borrow_status(r, "Rejected")
                )
                item.add_widget(accept_btn)
                item.add_widget(reject_btn)

            container.add_widget(item)

    def update_borrow_status(self, request_id, new_status):
        date_approved = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        if new_status == "Approved":
            # Get info from borrow_requests
            cursor.execute("""
                SELECT student_name, student_number, book_id, book_title, book_author, category
                FROM borrow_requests WHERE id=?
            """, (request_id,))
            request = cursor.fetchone()

            if request:
                student_name, student_number, book_id, book_title, book_author, category = request

                # Insert into borrowed_books with the new date
                cursor.execute("""
                    INSERT INTO borrowed_books (
                        student_name, student_number, book_id , book_title, book_author, category, date_borrowed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (student_name, student_number, book_id, book_title, book_author, category, date_approved))

                # After inserting to borrowed_books
                cursor.execute("""
                    UPDATE books
                    SET availability = 'Not Available'
                    WHERE title = ? AND author = ?
                """, (book_title, book_author))


        # Update the borrow_requests table
        cursor.execute("""
            UPDATE borrow_requests 
            SET status = ?, date_approved = ?
            WHERE id = ?
        """, (new_status, date_approved, request_id))

        conn.commit()
        conn.close()
        self.load_borrow_requests()

    # Student Dashboard
    def load_student_borrowed_books(self):
        screen = self.root.get_screen("view_borrowed_screen")
        container = screen.ids.student_borrowed_books_list
        container.clear_widgets()

        student_number = getattr(self, 'logged_in_student_number', None)
        if not student_number:
            self.show_generic_dialog("Login required.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT book_id, book_title, book_author, category, date_borrowed, date_returned, return_status
            FROM borrowed_books
            WHERE student_number = ?
        """, (student_number,))
        borrowed_books = cursor.fetchall()
        conn.close()

        for book_id, title, author, category, date_borrowed, date_returned, return_status in borrowed_books:
            item = MDListItem()
            item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant"))
            item.add_widget(MDListItemHeadlineText(text=f"{title}  |  {category}"))
            item.add_widget(MDListItemSupportingText(text=f"Author: {author}  |  status: {return_status}"))
            item.add_widget(MDListItemTertiaryText(text=f"Borrowed: {date_borrowed}  |  Returned: {date_returned}"))

            #  Show Return Button only if not yet returned
            if return_status != "Returned":
                return_btn = MDIconButton(
                    icon="book-arrow-left-outline",
                    theme_icon_color="Custom",
                    icon_color=(0.8, 0.2, 0, 1),
                    on_release=lambda x, bid=book_id, t=title, a=author, c=category: self.request_return_book(bid, t, a, c)

                )
                item.add_widget(return_btn)

            container.add_widget(item)

    # Librarian Dashboard
    def load_borrowed_books(self):
        screen = self.root.get_screen("view_borrowed_librarian_screen")
        container = screen.ids.borrowed_books_list
        container.clear_widgets()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT 
        student_name,
        student_number,
        book_id,
        book_title,
        book_author,
        category,
        date_borrowed,
        date_returned,
        return_status FROM borrowed_books""")
        rows = cursor.fetchall()
        conn.close()

        for name, number, book_id, title, author, category, date_borrowed, date_returned, return_status  in rows:
            item = MDListItem()
            item.add_widget(MDListItemLeadingIcon(icon="book-open-page-variant-outline"))
            item.add_widget(MDListItemHeadlineText(text=f"Student name: {name}  |  Student number: {number}"))
            item.add_widget(MDListItemSupportingText(text=f"Title: {title}  |  Author: {author}  |  {category}"))
            item.add_widget(MDListItemTertiaryText(text=f"Borrowed: {date_borrowed}  |  Status: {return_status}  |  Returned: {date_returned} "))
            container.add_widget(item)


    def build(self):
        self.insert_books_from_data()
        return Builder.load_file("library_app.kv")

if __name__ == "__main__":
    AnoWalangTutulong().run()
