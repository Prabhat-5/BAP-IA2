# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:19:34 2024

@author: Prabhat
"""
import tkinter as tk
import sqlite3

def reserve_ticket():
    customer_name = customer_name_entry.get()
    contact = contact_entry.get()
    address = address_entry.get()
    destination = destination_entry.get()
    number_plate = number_plate_entry.get()

    if customer_name == "" or destination == "" or number_plate == "":
        status_label.config(text="Please fill in all fields.", fg="red")
        return

    c.execute("INSERT INTO rental (customer_name, contact, address, destination, number_plate) VALUES (?, ?, ?, ?, ?)", (customer_name, contact, address, destination, number_plate))
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
        tk.Label(view_window, text=f"ID: {reservation[0]}, customer_name: {reservation[1]}, Destination: {reservation[4]}, number_plate: {reservation[5]}").grid(row=i, column=0, sticky="w")

def update_reservation():
    try:
        reservation_id = int(update_id_entry.get())
        customer_name = update_customer_name_entry.get()
        destination = update_destination_entry.get()
        number_plate = update_number_plate_entry.get()

        c.execute("UPDATE rental SET customer_name=?, destination=?, number_plate=? WHERE id=?", (customer_name, destination, number_plate, reservation_id))
        conn.commit()
        status_label.config(text="Reservation updated successfully.", fg="green")
    except ValueError:
        status_label.config(text="Please enter a valid reservation ID and number of number_plate.", fg="red")

# Connect to SQLite database
conn = sqlite3.connect('car_rental.db')
c = conn.cursor()

# Create rental table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS rental
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             customer_name TEXT,
             contact INTEGER,
             address TEXT,
             destination TEXT,
             number_plate TEXT)''')
conn.commit()

root = tk.Tk()
root.title("Car Rental Management System")
root.configure(bg="#00FFFF")

# Title label
title_label = tk.Label(root, text="Car Rental Management System", font=("Helvetica", 20), bg="#00FFFF")
title_label.pack(side="top", pady=20)

box = tk.Frame(root, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
box.pack()

# Reserve Ticket Section
reserve_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10)
reserve_frame.pack(pady=10)

tk.Label(reserve_frame, text="Customer Name:", bg="#e0e0e0").grid(row=0, column=0)
customer_name_entry = tk.Entry(reserve_frame)
customer_name_entry.grid(row=0, column=1)

tk.Label(reserve_frame, text="Contact:", bg="#e0e0e0").grid(row=1, column=0)
contact_entry = tk.Entry(reserve_frame)
contact_entry.grid(row=1, column=1)

tk.Label(reserve_frame, text="Address:", bg="#e0e0e0").grid(row=2, column=0)
address_entry = tk.Entry(reserve_frame)
address_entry.grid(row=2, column=1)

tk.Label(reserve_frame, text="Destination:", bg="#e0e0e0").grid(row=3, column=0)
destination_entry = tk.Entry(reserve_frame)
destination_entry.grid(row=3, column=1)

tk.Label(reserve_frame, text="Number of Number Plate:", bg="#e0e0e0").grid(row=4, column=0)
number_plate_entry = tk.Entry(reserve_frame)
number_plate_entry.grid(row=4, column=1)

tk.Button(reserve_frame, text="Reserve Ticket", command=reserve_ticket).grid(row=5, columnspan=2)

# Delete Section
delete_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10, bd=1, relief="solid")
delete_frame.pack(pady=10)

tk.Label(delete_frame, text="Delete Reservation by ID:", bg="#e0e0e0").pack()
delete_entry = tk.Entry(delete_frame)
delete_entry.pack()
tk.Button(delete_frame, text="Delete", command=delete).pack()

# Update Section
update_frame = tk.Frame(box, bg="#e0e0e0", padx=10, pady=10)
update_frame.pack(pady=10)

tk.Label(update_frame, text="Update Reservation (ID):", bg="#e0e0e0").pack()
update_id_entry = tk.Entry(update_frame)
update_id_entry.pack()

tk.Label(update_frame, text="Customer Name:", bg="#e0e0e0").pack()
update_customer_name_entry = tk.Entry(update_frame)
update_customer_name_entry.pack()

tk.Label(update_frame, text="Destination:", bg="#e0e0e0").pack()
update_destination_entry = tk.Entry(update_frame)
update_destination_entry.pack()

tk.Label(update_frame, text="Number of Number Plate:", bg="#e0e0e0").pack()
update_number_plate_entry = tk.Entry(update_frame)
update_number_plate_entry.pack()

tk.Button(update_frame, text="Update", command=update_reservation).pack()

# View Reservations Section
view_button = tk.Button(root, text="View All Reservations", command=views)
view_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()

# Close database connection
conn.close()

