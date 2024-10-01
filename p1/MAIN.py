import tkinter as tk
from tkinter import messagebox
import json
import os

# Class to manage the book store
class BookStore:
    def __init__(self, data_file='books.json'):
        self.data_file = data_file
        self.books = self.load_data()

    # Load book data from a file
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    # Save book data to a file
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.books, f, indent=4)

    # Add a new book with validation
    def add_book(self, title, author, price, quantity):
        if not title or not author or not price or not quantity:
            return False, "All fields must be filled out!"
        if title in self.books:
            return False, "Book already exists!"
        try:
            price = float(price)
            quantity = int(quantity)
            if price < 0 or quantity < 0:
                return False, "Price and quantity must be non-negative!"
        except ValueError:
            return False, "Price must be a number and quantity must be an integer!"

        self.books[title] = {'author': author, 'price': price, 'quantity': quantity}
        self.save_data()
        return True, "Book added successfully!"

    # View all books
    def view_books(self):
        return self.books

    # Search for a book
    def search_books(self, search_term):
        return {title: info for title, info in self.books.items() if search_term.lower() in title.lower()}

    # Purchase a book
    def purchase_book(self, title, quantity):
        if title in self.books:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    return False, "Quantity must be a positive integer!"
            except ValueError:
                return False, "Quantity must be an integer!"
            
            if self.books[title]['quantity'] >= quantity:
                self.books[title]['quantity'] -= quantity
                self.save_data()
                return True, f"Purchased {quantity} copies of '{title}'."
            else:
                return False, "Insufficient stock!"
        else:
            return False, "Book not found!"

    # Delete a book
    def delete_book(self, title):
        if title in self.books:
            del self.books[title]
            self.save_data()
            return True, "Book deleted successfully!"
        return False, "Book not found!"
# Main application class for the GUI
class BookStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Book Store")
        self.root.geometry("600x600")
        self.book_store = BookStore()

        # Create the main menu frame
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(pady=50)

        tk.Label(self.main_menu_frame, text="Online Book Store", font=('Arial', 16)).pack()
        tk.Button(self.main_menu_frame, text="Add Book", command=self.show_add_book).pack(pady=10)
        tk.Button(self.main_menu_frame, text="View Books", command=self.show_books).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Purchase Book", command=self.show_purchase_book).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Delete Book", command=self.show_delete_book).pack(pady=10)

        # Create add book frame
        self.add_book_frame = tk.Frame(self.root)

        # Create view books frame
        self.view_books_frame = tk.Frame(self.root)

        # Create purchase book frame
        self.purchase_book_frame = tk.Frame(self.root)

        # Create delete book frame
        self.delete_book_frame = tk.Frame(self.root)

    def show_add_book(self):
        self.hide_all_frames()
        self.add_book_frame.pack(pady=50)
        self.create_add_book_widgets()

    def create_add_book_widgets(self):
        # Clear previous widgets if any
        for widget in self.add_book_frame.winfo_children():
            widget.destroy()

        tk.Label(self.add_book_frame, text="Add New Book", font=('Arial', 16)).pack(pady=10)
        
        tk.Label(self.add_book_frame, text="Title").pack()
        self.title_entry = tk.Entry(self.add_book_frame, width=50)
        self.title_entry.pack(pady=5)

        tk.Label(self.add_book_frame, text="Author").pack()
        self.author_entry = tk.Entry(self.add_book_frame, width=50)
        self.author_entry.pack(pady=5)

        tk.Label(self.add_book_frame, text="Price").pack()
        self.price_entry = tk.Entry(self.add_book_frame, width=50)
        self.price_entry.pack(pady=5)

        tk.Label(self.add_book_frame, text="Quantity").pack()
        self.quantity_entry = tk.Entry(self.add_book_frame, width=50)
        self.quantity_entry.pack(pady=5)

        tk.Button(self.add_book_frame, text="Submit", command=self.add_book).pack(pady=10)
        tk.Button(self.add_book_frame, text="Back to Menu", command=self.show_main_menu).pack()

    def show_books(self):
        self.hide_all_frames()
        self.view_books_frame.pack(pady=50)
        self.create_view_books_widgets()

    def create_view_books_widgets(self):
        # Clear previous widgets if any
        for widget in self.view_books_frame.winfo_children():
            widget.destroy()

        tk.Label(self.view_books_frame, text="Available Books", font=('Arial', 16)).pack(pady=10)
        self.books_listbox = tk.Listbox(self.view_books_frame, width=80, height=20)
        self.books_listbox.pack(pady=10)

        self.refresh_books_listbox()

        tk.Button(self.view_books_frame, text="Back to Menu", command=self.show_main_menu).pack(pady=10)

    def refresh_books_listbox(self):
        self.books_listbox.delete(0, tk.END)  # Clear existing list
        books = self.book_store.view_books()
        if not books:
            self.books_listbox.insert(tk.END, "No books available.")
        else:
            for title, info in books.items():
                self.books_listbox.insert(tk.END, f"Title: {title}, Author: {info['author']}, Price: ${info['price']:.2f}, Quantity: {info['quantity']}")

    def show_purchase_book(self):
        self.hide_all_frames()
        self.purchase_book_frame.pack(pady=50)
        self.create_purchase_book_widgets()

    def create_purchase_book_widgets(self):
        # Clear previous widgets if any
        for widget in self.purchase_book_frame.winfo_children():
            widget.destroy()

        tk.Label(self.purchase_book_frame, text="Purchase Book", font=('Arial', 16)).pack(pady=10)
        
        tk.Label(self.purchase_book_frame, text="Title").pack()
        self.purchase_title_entry = tk.Entry(self.purchase_book_frame, width=50)
        self.purchase_title_entry.pack(pady=5)

        tk.Label(self.purchase_book_frame, text="Quantity").pack()
        self.purchase_quantity_entry = tk.Entry(self.purchase_book_frame, width=50)
        self.purchase_quantity_entry.pack(pady=5)

        tk.Button(self.purchase_book_frame, text="Submit", command=self.purchase_book).pack(pady=10)
        tk.Button(self.purchase_book_frame, text="Back to Menu", command=self.show_main_menu).pack()

    def show_delete_book(self):
        self.hide_all_frames()
        self.delete_book_frame.pack(pady=50)
        self.create_delete_book_widgets()

    def create_delete_book_widgets(self):
        # Clear previous widgets if any
        for widget in self.delete_book_frame.winfo_children():
            widget.destroy()

        tk.Label(self.delete_book_frame, text="Delete Book", font=('Arial', 16)).pack(pady=10)
        
        tk.Label(self.delete_book_frame, text="Title").pack()
        self.delete_title_entry = tk.Entry(self.delete_book_frame, width=50)
        self.delete_title_entry.pack(pady=5)

        tk.Button(self.delete_book_frame, text="Delete", command=self.delete_book).pack(pady=10)
        tk.Button(self.delete_book_frame, text="Back to Menu", command=self.show_main_menu).pack()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        success, message = self.book_store.add_book(title, author, price, quantity)

        if success:
            messagebox.showinfo("Success", message)
            self.show_main_menu()
        else:
            messagebox.showerror("Error", message)

    def purchase_book(self):
        title = self.purchase_title_entry.get().strip()
        quantity = self.purchase_quantity_entry.get().strip()

        success, message = self.book_store.purchase_book(title, quantity)

        if success:
            messagebox.showinfo("Success", message)
            self.show_main_menu()
        else:
            messagebox.showerror("Error", message)

    def delete_book(self):
        title = self.delete_title_entry.get().strip()
        success, message = self.book_store.delete_book(title)

        if success:
            messagebox.showinfo("Success", message)
            self.show_main_menu()
        else:
            messagebox.showerror("Error", message)

    def show_main_menu(self):
        self.hide_all_frames()
        self.main_menu_frame.pack(pady=50)

    def hide_all_frames(self):
        self.main_menu_frame.pack_forget()
        self.add_book_frame.pack_forget()
        self.view_books_frame.pack_forget()
        self.purchase_book_frame.pack_forget()
        self.delete_book_frame.pack_forget()

# Run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookStoreApp(root)
    root.mainloop()
