import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('details.db')
    cursor = conn.cursor()
    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            aadhaar TEXT,
            pan TEXT,
            mobile TEXT
        )
    ''')
    conn.commit()
    conn.close()

# GUI 1: Upload Data
def upload_data():
    def submit_data():
        name = entry_name.get().strip()
        surname = entry_surname.get().strip()
        aadhaar = entry_aadhaar.get().strip()
        pan = entry_pan.get().strip()
        mobile = entry_mobile.get().strip()

        if not name or not surname:
            messagebox.showerror("Error", "Name and Surname are required!")
            return

        try:
            conn = sqlite3.connect('details.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, surname, aadhaar, pan, mobile)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, surname, aadhaar, pan, mobile))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Details uploaded successfully!")
            clear_form()

            # Show the main screen again after form submission
            form_window.pack_forget()
            main_screen.pack()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_form():
        entry_name.delete(0, tk.END)
        entry_surname.delete(0, tk.END)
        entry_aadhaar.delete(0, tk.END)
        entry_pan.delete(0, tk.END)
        entry_mobile.delete(0, tk.END)

    # Hide the main screen
    main_screen.pack_forget()

    # Create the upload form window
    form_window = tk.Frame(root, bg='#f0f0f0')  # Set background color of the form window
    form_window.pack()

    tk.Label(form_window, text="Name", bg='#f0f0f0', fg='blue').grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(form_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Surname", bg='#f0f0f0', fg='blue').grid(row=1, column=0, padx=10, pady=5)
    entry_surname = tk.Entry(form_window)
    entry_surname.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Aadhaar Card", bg='#f0f0f0', fg='blue').grid(row=2, column=0, padx=10, pady=5)
    entry_aadhaar = tk.Entry(form_window)
    entry_aadhaar.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_window, text="PAN Card", bg='#f0f0f0', fg='blue').grid(row=3, column=0, padx=10, pady=5)
    entry_pan = tk.Entry(form_window)
    entry_pan.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_window, text="Mobile Number", bg='#f0f0f0', fg='blue').grid(row=4, column=0, padx=10, pady=5)
    entry_mobile = tk.Entry(form_window)
    entry_mobile.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(form_window, text="Submit", command=submit_data, bg='#4CAF50', fg='white').grid(row=5, column=0, columnspan=2, pady=10)

# GUI 2: Retrieve Data
def retrieve_data():
    def search_data():
        name = entry_name.get().strip()
        surname = entry_surname.get().strip()

        if not name or not surname:
            messagebox.showerror("Error", "Name and Surname are required!")
            return

        try:
            conn = sqlite3.connect('details.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE LOWER(name) = ? AND LOWER(surname) = ?
            ''', (name.lower(), surname.lower()))
            result = cursor.fetchone()
            conn.close()

            if result:
                output = f"Name: {result[1]}\nSurname: {result[2]}\nAadhaar: {result[3]}\nPAN: {result[4]}\nMobile: {result[5]}"
                messagebox.showinfo("Details Found", output)

                # Hide the retrieve screen and show the main screen again
                retrieve_window.pack_forget()
                main_screen.pack()
            else:
                messagebox.showerror("Error", "No details found for the given name and surname.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Hide the main screen
    main_screen.pack_forget()

    # Create the retrieve form window
    retrieve_window = tk.Frame(root, bg='#f0f0f0')  # Set background color of the form window
    retrieve_window.pack()

    tk.Label(retrieve_window, text="Name", bg='#f0f0f0', fg='blue').grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(retrieve_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(retrieve_window, text="Surname", bg='#f0f0f0', fg='blue').grid(row=1, column=0, padx=10, pady=5)
    entry_surname = tk.Entry(retrieve_window)
    entry_surname.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(retrieve_window, text="Search", command=search_data, bg='#4CAF50', fg='white').grid(row=2, column=0, columnspan=2, pady=10)

# Main Menu
root = tk.Tk()
root.title("Details Management System")
root.geometry("400x300")  # Set the main window size
root.config(bg='#f0f0f0')  # Set background color for the main window

# Initialize database
initialize_database()

# Main Screen (Upload and Retrieve buttons)
main_screen = tk.Frame(root, bg='#f0f0f0')  # Set background color for main screen
main_screen.pack()

tk.Button(main_screen, text="Upload Details", command=upload_data, width=20, bg='#4CAF50', fg='white').pack(pady=10)
tk.Button(main_screen, text="Retrieve Details", command=retrieve_data, width=20, bg='#4CAF50', fg='white').pack(pady=10)

root.mainloop()
