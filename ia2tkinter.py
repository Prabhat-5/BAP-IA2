# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:19:34 2024

@author: Prabhat
"""

import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('carr_rental.db')
c = conn.cursor()

# Create rental table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS rental
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             customer_name TEXT,
             contact INTEGER,
             address TEXT,
             destination TEXT,
             car_model TEXT,
             rental_hours INTEGER)''')

def book_car():
    customer_name = customer_name_entry.get()
    contact = contact_entry.get()
    address = address_entry.get()
    destination = destination_entry.get()
    car_model = car_model_var.get()  # Get the selected car model from the dropdown
    rental_hours = rental_hours_var.get()  # Get the selected rental hours from the dropdown

    if customer_name == "" or destination == "" or car_model == "" or rental_hours == "":
        status_label.config(text="Please fill in all fields.", fg="red")
        return

    c.execute("INSERT INTO rental (customer_name, contact, address, destination, car_model, rental_hours) VALUES (?, ?, ?, ?, ?, ?)",
              (customer_name, contact, address, destination, car_model, rental_hours))
    conn.commit()
    status_label.config(text="Ticket reserved successfully.", fg="green")

def delete():
    try:
        reservation_id = int(delete_entry.get())
        c.execute("DELETE FROM rental WHERE id=?", (reservation_id,))
        conn.commit()
        status_label.config(text="Reservation deleted successfully.", fg="green")
    except ValueError:
        status_label.config(text="Please enter a valid reservation ID.", fg="red")

def views():
    view_window = tk.Toplevel(root)
    view_window.title("All Reservations")

    c.execute("SELECT * FROM rental")
    reservations = c.fetchall()

    for i in range(len(reservations)):
        reservation = reservations[i]
        tk.Label(view_window, text=f"ID: {reservation[0]}, customer_name: {reservation[1]}, Contact: {reservation[2]}, Destination: {reservation[4]}, car_model: {reservation[5]}, Rental Hours: {reservation[6]}").grid(row=i, column=0, sticky="w")

def update_booking():
    try:
        reservation_id = int(update_id_entry.get())
        customer_name = update_customer_name_entry.get()
        destination = update_destination_entry.get()
        car_model = update_car_model_var.get()  # Get the selected car model from the dropdown
        rental_hours = update_rental_hours_var.get()

        # Use parameterized query to prevent SQL injection
        c.execute("UPDATE rental SET customer_name=?, destination=?, car_model=?, rental_hours=? WHERE id=?", (customer_name, destination, car_model, rental_hours, reservation_id))
        conn.commit()
        status_label.config(text="Reservation updated successfully.", fg="green")
    except ValueError:
        status_label.config(text="Please enter a valid reservation ID, car model, and rental hours.", fg="red")

def calculate_bill(car_model, rental_hours):
    # Define the rates per hour for each car model
    rates_per_hour = {
        "Toyota": 1000,
        "Honda": 1200,
        "Nissan": 1100,
        "Ford": 1300,
        "Chevrolet": 1400
    }
    
    # Calculate the total cost
    rate_per_hour = rates_per_hour.get(car_model, 0)  # Get the rate per hour for the selected car model
    total_cost = rate_per_hour * rental_hours
    
    return total_cost

def generate_bill():
    try:
        reservation_id = int(billing_id_entry.get())
        c.execute("SELECT car_model, rental_hours FROM rental WHERE id=?", (reservation_id,))
        reservation_data = c.fetchone()
        if reservation_data:
            car_model, rental_hours = reservation_data
            total_cost = calculate_bill(car_model, rental_hours)
            bill_text = f"Reservation ID: {reservation_id}\nCar Model: {car_model}\nRental Hours: {rental_hours}\nTotal Cost: Rs.{total_cost}"
            bill_textbox.config(state="normal")
            bill_textbox.delete("1.0", tk.END)
            bill_textbox.insert(tk.END, bill_text)
            bill_textbox.config(state="disabled")
            status_label.config(text="Bill generated successfully.", fg="green")
        else:
            status_label.config(text="Reservation ID not found.", fg="red")
    except ValueError:
        status_label.config(text="Please enter a valid reservation ID.", fg="red")

root = tk.Tk()
root.title("Car Rental Management System")
root.configure(bg="#FFFFFF")

# Title label
title_label = tk.Label(root, text="Car Rental Management System", font=("Helvetica", 20), bg="#FFFFFF")
title_label.pack(side="top", pady=20)

# Box for viewing, adding, deleting, and updating
box = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10, bd=1, relief="solid")
box.pack(pady=20)



# Add Section
add_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
add_frame.grid(row=0, column=1, padx=5)

tk.Label(add_frame, text="Add Reservation", bg="#e0e0e0").pack()
tk.Label(add_frame, text="Customer Name:").pack()
customer_name_entry = tk.Entry(add_frame)
customer_name_entry.pack()
tk.Label(add_frame, text="Contact:").pack()
contact_entry = tk.Entry(add_frame)
contact_entry.pack()
tk.Label(add_frame, text="Address:").pack()
address_entry = tk.Entry(add_frame)
address_entry.pack()
tk.Label(add_frame, text="Destination:").pack()
destination_entry = tk.Entry(add_frame)
destination_entry.pack()
tk.Label(add_frame, text="Car Model:").pack()
car_model_var = tk.StringVar()
car_model_dropdown = ttk.Combobox(add_frame, textvariable=car_model_var, values=["Toyota    --  1000/hr", "Honda    --  1200/hr", "Nissan   --  1100/hr", "Ford     --  1300/hr", "Chevrolet --  1400/hr"])
car_model_dropdown.pack()
tk.Label(add_frame, text="Rental Hours:").pack()
rental_hours_var = tk.StringVar()
rental_hours_dropdown = ttk.Combobox(add_frame, textvariable=rental_hours_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
rental_hours_dropdown.pack()
add_button = tk.Button(add_frame, text="Add", command=book_car)
add_button.pack()



# Update Section
update_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
update_frame.grid(row=0, column=3, padx=10)

tk.Label(update_frame, text="Update Reservation", bg="#e0e0e0").pack()
tk.Label(update_frame, text="Reservation ID:").pack()
update_id_entry = tk.Entry(update_frame)
update_id_entry.pack()
tk.Label(update_frame, text="Customer Name:").pack()
update_customer_name_entry = tk.Entry(update_frame)
update_customer_name_entry.pack()
tk.Label(update_frame, text="Destination:").pack()
update_destination_entry = tk.Entry(update_frame)
update_destination_entry.pack()
tk.Label(update_frame, text="Car Model:").pack()
update_car_model_var = tk.StringVar()
update_car_model_dropdown = ttk.Combobox(update_frame, textvariable=update_car_model_var, values=["Toyota", "Honda", "Nissan", "Ford", "Chevrolet"])
update_car_model_dropdown.pack()
tk.Label(update_frame, text="Rental Hours:").pack()
update_rental_hours_var = tk.StringVar()
update_rental_hours_dropdown = ttk.Combobox(update_frame, textvariable=update_rental_hours_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
update_rental_hours_dropdown.pack()
update_button = tk.Button(update_frame, text="Update", command=update_booking)
update_button.pack()

# View Section
view_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
view_frame.grid(row=1, column=1, padx=10)

view_button = tk.Button(view_frame, text="View Bookings", command=views)
view_button.pack()

# Delete Section
delete_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
delete_frame.grid(row=1, column=3, padx=10)

tk.Label(delete_frame, text="Delete Reservation", bg="#e0e0e0").pack()
tk.Label(delete_frame, text="Reservation ID:").pack()
delete_entry = tk.Entry(delete_frame)
delete_entry.pack()
delete_button = tk.Button(delete_frame, text="Delete", command=delete)
delete_button.pack()

# Billing Section
billing_frame = tk.Frame(root, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
billing_frame.pack(pady=20)

tk.Label(billing_frame, text="Generate Bill", bg="#e0e0e0").pack()
tk.Label(billing_frame, text="Reservation ID:").pack()
billing_id_entry = tk.Entry(billing_frame)
billing_id_entry.pack()
generate_bill_button = tk.Button(billing_frame, text="Generate Bill", command=generate_bill)
generate_bill_button.pack()
bill_textbox = tk.Text(billing_frame, height=6, width=40)
bill_textbox.pack()
bill_textbox.config(state="disabled")

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()

# Close database connection
conn.close()
