import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Function to create a connection to the MySQL database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='BBBSHYAW', 
            database='restaurant' 
        )
    except:
        print("The error occurred")
        return None
    return connection

# Function to fetch and display customers in the listbox
def fetch_customers():
    connection = create_connection()
    if connection is None:
        messagebox.showerror("Database Error", "Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers")
        records = cursor.fetchall()

        # Clear the listbox
        listbox.delete(0, tk.END)

        # Insert records into the listbox
        for record in records:
            listbox.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Date: {record[2]}, Time: {record[3]}, Money Spent: {record[4]}")

    except Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to fetch and display customers by date in the listbox
def fetch_customers_by_month():
    date = fetch_entry.get()
    if not date:
        messagebox.showerror("Error", "Please enter a month (YYYY-MM).")
        return

    connection = create_connection()
    if connection is None:
        messagebox.showerror("Database Error", "Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE visit_date LIKE %s", (f"{date}%",))
        records = cursor.fetchall()

        # Clear the listbox
        listbox.delete(0, tk.END)

        # Insert records into the listbox
        for record in records:
            listbox.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Date: {record[2]}, Time: {record[3]}, Money Spent: {record[4]}")

    except Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to clear the month filter
def clear_month_filter():
    fetch_entry.delete(0, tk.END)
    fetch_customers()

# Function to submit data to the database
def submit_data():
    name = name_entry.get()
    money_spent = money_entry.get()
    
    # Get current date and time
    if not date_entry.get():
        visit_date = datetime.now().date()
    else:
        visit_date = date_entry.get()
        date_entry.get() == 0
    visit_time = datetime.now().time().strftime('%H:%M:%S')

    if name and money_spent:
        connection = create_connection()
        if connection is None:
            messagebox.showerror("Database Error", "Could not connect to the database.")
            return

        try:
            cursor = connection.cursor()
            # Insert data into the database
            cursor.execute('''INSERT INTO customers (name, visit_date, visit_time, money_spent) VALUES (%s, %s, %s, %s)''', (name, visit_date, visit_time, float(money_spent)))
            connection.commit()
            name_entry.delete(0, tk.END)
            money_entry.delete(0, tk.END)
            date_entry.delete(0,tk.END)

            # Update the customer list
            fetch_customers()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount for money spent.")
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

# Function to delete a selected customer
def delete_customer():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a customer to delete.")
        return

    selected_customer = listbox.get(selected[0])
    customer_id = selected_customer.split(",")[0].split(":")[1].strip()  # Extract ID from the selected string

    connection = create_connection()
    if connection is None:
        messagebox.showerror("Database Error", "Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        connection.commit()
        
        # Update the customer list
        fetch_customers()
    except Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_database_and_table_if_not_exists(db_name):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='BBBSHYAW'  
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the database already exists
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()

            if not result:
                cursor.execute(f"CREATE DATABASE {db_name}")
            connection.database = db_name
            cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                visit_date DATE NOT NULL,
                visit_time TIME NOT NULL,
                money_spent DECIMAL(10, 2) NOT NULL
            )''')

    except:
        print("The error occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Call the function to create a database and the customers table
create_database_and_table_if_not_exists('restaurant')
# Create the main window
root = tk.Tk()
root.title("Restaurant Customer Data")
root.geometry("600x400")#size of screen
root.configure(bg="#FFFF00")#background color

# Create and place the main frame
main_frame = tk.Frame(root, bg="#f0f0f0", padx =10, pady=10)
main_frame.pack(padx=10, pady=10)

# Create and place the labels and entries
tk.Label(main_frame, text="Customer Name:", bg="#f0f0f0").grid(row=0, column=0, sticky='w', pady=5)
name_entry = tk.Entry(main_frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(main_frame, text="Money Spent:", bg="#f0f0f0").grid(row=1, column=0, sticky='w', pady=5)
money_entry = tk.Entry(main_frame, width=30)
money_entry.grid(row=1, column=1, pady=5)

tk.Label(main_frame, text="date(input) (YYYY-MM-DD):", bg="#f0f0f0").grid(row=2, column=0, sticky='w', pady=5)
date_entry = tk.Entry(main_frame, width=30)
date_entry.grid(row=2, column=1, pady=5)

tk.Label(main_frame, text="date(to fetch by dates) (YYYY-MM-DD):", bg="#f0f0f0").grid(row=3, column=0, sticky='w', pady=5)
fetch_entry = tk.Entry(main_frame, width=30)
fetch_entry.grid(row=3, column=1, pady=5)

# Create and place the buttons
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.grid(row = 4, columnspan=2, pady=10)

submit_button = tk.Button(button_frame, text="Submit", command=submit_data, bg="#4CAF50", fg="white", width=10)
submit_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, text="Delete", command=delete_customer, bg="#F44336", fg="white", width=10)
delete_button.grid(row=0, column=1, padx=5)

month_button = tk.Button(button_frame, text="Fetch by date", command=fetch_customers_by_month, bg="#4CAF50", fg="white", width=10)
month_button.grid(row=0, column=2, padx =5)

clear_button = tk.Button(button_frame, text="Clear Filter", command=clear_month_filter, bg="#F44336", fg="white", width=10)
clear_button.grid(row=0, column=3, padx=5)

# Create and place the listbox to display customers
listbox = tk.Listbox(main_frame, width=70, height=10)
listbox.grid(row=5, columnspan=2, pady=10)

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(main_frame)
scrollbar.grid(row=4, column=2, sticky='ns')

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Fetch initial customer data
fetch_customers()

# Start the Tkinter event loop
root.mainloop()