import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random

def rent_car():
    customer_name = customer_name_entry.get()
    age = age_entry.get()
    license_image = license_image_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    car_name = car_combobox.get()
    rental_hours = rental_hours_entry.get()

    if customer_name == "" or age == "" or phone == "" or email == "" or car_name == "" or rental_hours == "":
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    # Extract price from car name
    price_per_hour = int(car_name.split("$")[1])

    rental_hours = int(rental_hours)
    total_cost = price_per_hour * rental_hours

    bill_text = f"BILL\n"
    bill_text += f"Car Model        : {car_name}\n"
    bill_text += f"Price per Hour : ${price_per_hour}\n"
    bill_text += f"No of Hours     : {rental_hours}\n"
    bill_text += f"Total Cost       : ${total_cost}"
    bill_label.config(text=bill_text)

    payment_button.config(state="normal")

def process_payment():
    card_number = card_number_entry.get()
    expiry_date = expiry_date_entry.get()
    cvv = cvv_entry.get()

    if card_number == "" or expiry_date == "" or cvv == "":
        messagebox.showwarning("Warning", "Please fill in all payment details.")
        return

    messagebox.showinfo("Payment Successful", "Payment was successful!")
    clear_entries()

def clear_entries():
    customer_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    license_image_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    rental_hours_entry.delete(0, tk.END)
    car_combobox.set("")
    bill_label.config(text="")
    payment_button.config(state="disabled")

def browse_image():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if filename:
        license_image_entry.delete(0, tk.END)
        license_image_entry.insert(tk.END, filename)

root = tk.Tk()
root.title("Car Rental System")
root.geometry("500x600")
root.resizable(True, True)

heading_label = tk.Label(root, text="RENT YOUR CAR!", font=("Arial", 18, "bold"), pady=10)
heading_label.pack()

main_frame = tk.Frame(root, bg="lightblue")
main_frame.pack(pady=20)

tk.Label(main_frame, text="Customer Name:", bg="lightblue", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Age:", bg="lightblue", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="License Image:", bg="lightblue", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Phone:", bg="lightblue", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Email:", bg="lightblue", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Select Car:", bg="lightblue", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Rental Hours:", bg="lightblue", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="w")

customer_name_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
customer_name_entry.grid(row=0, column=1, padx=10, pady=5)
age_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
age_entry.grid(row=1, column=1, padx=10, pady=5)
license_image_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
license_image_entry.grid(row=2, column=1, padx=10, pady=5)
phone_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
phone_entry.grid(row=3, column=1, padx=10, pady=5)
email_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
email_entry.grid(row=4, column=1, padx=10, pady=5)

browse_button = tk.Button(main_frame, text="Browse", command=browse_image, font=("Arial", 10))
browse_button.grid(row=2, column=2, padx=5)

car_combobox = ttk.Combobox(main_frame, width=27, state="readonly", font=("Arial", 12))
car_combobox.grid(row=5, column=1, padx=10, pady=5)
car_combobox['values'] = ("Toyota Corolla $100", "Honda Civic $200", "Ford Mustang $800", "Jeep Wrangler $500", "Chevy Tahoe $650")

rental_hours_entry = tk.Entry(main_frame, width=30, font=("Arial", 12))
rental_hours_entry.grid(row=6, column=1, padx=10, pady=5)

rent_car_button = tk.Button(main_frame, text="Rent Car", command=rent_car, font=("Arial", 12))
rent_car_button.grid(row=7, columnspan=2, pady=10)

bill_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="lightblue", justify=tk.LEFT)
bill_label.grid(row=8, columnspan=2, padx=10, pady=5, sticky="w")

payment_frame = tk.Frame(root, bg="lightblue")
payment_frame.pack(pady=20)

tk.Label(payment_frame, text="Card Number:", bg="lightblue", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
card_number_entry = tk.Entry(payment_frame, width=30, font=("Arial", 12))
card_number_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Label(payment_frame, text="Expiry Date:", bg="lightblue", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
expiry_date_entry = tk.Entry(payment_frame, width=30, font=("Arial", 12))
expiry_date_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Label(payment_frame, text="CVV:", bg="lightblue", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
cvv_entry = tk.Entry(payment_frame, width=30, font=("Arial", 12))
cvv_entry.grid(row=2, column=1, padx=10, pady=5)

payment_button = tk.Button(payment_frame, text="Make Payment", command=process_payment, state="disabled", font=("Arial", 12))
payment_button.grid(row=3, columnspan=2, pady=10)

root.mainloop()
