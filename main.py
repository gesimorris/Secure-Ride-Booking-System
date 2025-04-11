import tkinter as tk
from tkinter import messagebox
from digital_signature import sign_message, verify_signature
from rsa import generateKeys
from aes import encrypt_ride_data, decrypt_ride_data
from blockchain import Blockchain
import bcrypt
import json
import os
import random

# For accepted rides
accepted_rides = []

# Generate RSA keys
rider_public_key, rider_private_key = generateKeys()
driver_public_key, driver_private_key = generateKeys()

# Generate AES key
aes_key = os.urandom(16)

# Intitialize blockchain
blockchain = Blockchain()

# Function to handle login
def handle_login():
    username = entry4.get()
    messagebox.showinfo("Enter your username:", f"Username: {username}")

    password = entry5.get()
    messagebox.showinfo("Enter your password", f"Password: {password}")

    with open('users.json', 'r') as f:
        users = json.load(f)

        for user in users["users"]:
            if user["username"] == username:
                if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                    messagebox.showinfo("Login", "You have successfully logged in!")
                    open_menu(user["role"])
                else:
                    messagebox.showinfo("Login", "Invalid password. Please try again.")
                   
# Function to handle registration
def handle_register(): 
    username = entry.get()
    messagebox.showinfo("Enter your username:", f"Username: {username}")

    password = entry2.get()
    messagebox.showinfo("Enter your password", f"Password: {password}")

    role = entry3.get()
    messagebox.showinfo("Enter your role", f"Role: {role}")

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Create users.json if it doesn't exist
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({"users": []}, f) 

    # Read existing users in the file
    with open("users.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {"users": []} 

    # Add new user
    data["users"].append({"username": username, "password": hashed_pw, "role": role})

    # Write back to file
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)
    
    messagebox.showinfo("Registration", "Registration successful! You can now log in.")
    
# Function to open the menu based on user role
def open_menu(role):
    menu_window = tk.Toplevel(root)
    menu_window.title("Ride Booking Menu")
    
    if role == "rider":
        tk.Label(menu_window, text="Welcome Rider!").pack(pady=5)
        tk.Label(menu_window, text="Want to book a ride?").pack(pady=5)
        tk.Label(menu_window, text="Enter pickup location:").pack(pady=5)
        pickup = tk.Entry(menu_window, width=30)
        pickup.pack(pady=5)
        tk.Label(menu_window, text="Enter drop location:").pack(pady=5)
        drop = tk.Entry(menu_window, width=30)
        drop.pack(pady=5)
        tk.Label(menu_window, text="Enter vehicle type (Economy,Premium,SUV):").pack(pady=5)
        vehicle = tk.Entry(menu_window, width=30)
        vehicle.pack(pady=5)

        estimated_fare = round(random.uniform(10, 50), 2)
        tk.Label(menu_window, text=f"Estimated fare: ${estimated_fare}").pack(pady=5)
        
        tk.Label(menu_window, text="Confirm Booking? Y/N:").pack(pady=5)
        confirm = tk.Entry(menu_window, width=30)
        confirm.pack(pady=5)

        tk.Button(menu_window, text="Confirm", command=lambda: handle_confirm(pickup, drop, vehicle, confirm, estimated_fare)).pack(pady=5)
            
        
        tk.Button(menu_window, text="View Ride History", command=view_ride_history).pack(pady=5)
    elif role == "driver":
        tk.Label(menu_window, text="Welcome Driver!").pack(pady=5)
        tk.Label(menu_window, text="Looking for rides? Accept a ride request").pack(pady=5)
        tk.Button(menu_window, text="Accept a ride", command=lambda: view_requested_rides(menu_window)).pack(pady=5)
        tk.Label(menu_window, text="View your accepted rides").pack(pady=5)
        tk.Button(menu_window, text="My Rides", command=lambda: view_assigned_rides(menu_window)).pack(pady=5)
    
    tk.Button(menu_window, text="Logout", command=menu_window.destroy).pack(pady=5)

# Function to handle ride confirmation
def handle_confirm(pickup, drop, vehicle, confirm, estimated_fare):
        pickup = pickup.get()
        drop = drop.get()
        vehicle = vehicle.get()
        confirm_entry = confirm.get().lower()
        
        if confirm_entry == "y":
            ride_data = f"{pickup}|{drop}|{vehicle}|{estimated_fare}"
            # Sign the ride data with the private key
            signature = sign_message(ride_data, rider_private_key)
            # Encrypt using AES
            encrypted_data = encrypt_ride_data(ride_data, aes_key)
            # Add the transaction to the blockchain
            blockchain.add_transaction(encrypted_data, json.dumps(signature), str(rider_public_key))
            tk.messagebox.showinfo("Ride Confirmation", "Ride confirmed!")
        else:
            tk.messagebox.showinfo("Ride Confirmation", "Ride cancelled.")
            
# Function to view ride history
def view_ride_history():
    if not blockchain.chain:
        messagebox.showinfo("Ride History", "No rides found.")
        open_menu("rider")
    
    transaction = blockchain.chain[-1]
    ride_encrypted_data = bytes.fromhex(transaction['ride_data'])
    ride_signature = json.loads(transaction['signature'])
    rider_public_key = eval(transaction['rider_public_key'])
    decrypted_data = decrypt_ride_data(ride_encrypted_data, aes_key)
    if verify_signature(decrypted_data, ride_signature, rider_public_key):
        messagebox.showinfo("Ride History", f"Ride details: {decrypted_data}")
    else:
        messagebox.showinfo("Ride History", "No rides found.")

# Function to view requested rides
def view_requested_rides(menu_window):
    rides = []

    for block in blockchain.chain:
        try:
            encrypted_data = bytes.fromhex(block['ride_data'])
            signature = json.loads(block['signature'])
            key = eval(block['rider_public_key'])

            # Decrypt the ride data
            decrypted_data = decrypt_ride_data(encrypted_data, aes_key)
            # Verify the signature
            if verify_signature(decrypted_data, signature, key):
                rides.append(decrypted_data)
        except Exception as e:
            pass
    if not rides:
        messagebox.showinfo("Ride Requests", "No ride requests found.")
    
    ride_window = tk.Toplevel(menu_window)
    ride_window.title("Ride Requests")
    ride_listbox = tk.Listbox(ride_window , width=50, height=10)
    for  x, ride in enumerate(rides):
        ride_listbox.insert(x, ride)
    ride_listbox.pack(pady=5)
    tk.Button(ride_window, text="Assign Ride", command=lambda: accept_ride(ride_listbox, rides, ride_window)).pack(pady=5)

# Function to view accepted rides
def view_assigned_rides(menu_window):
    if not accepted_rides:
        messagebox.showinfo("Accepted Rides", "No accepted rides found.")
        return
    
    ride_window = tk.Toplevel(menu_window)
    ride_window.title("Accepted Rides")
    ride_listbox = tk.Listbox(ride_window , width=50, height=10)
    for  x, ride in enumerate(accepted_rides):
        ride_listbox.insert(x, ride)
    ride_listbox.pack(pady=5)
    tk.Button(ride_window, text="Close", command=ride_window.destroy).pack(pady=5)

# Function to view assigned rides
def accept_ride(ride_listbox, rides, ride_window):
    try:
        selected_index = ride_listbox.curselection()[0]
        selected_ride = rides[selected_index]
        # Change status to accepted
        if selected_ride in accepted_rides:
            tk.messagebox.showerror("Error", "Ride already accepted.")
            return
        accepted_rides.append(selected_ride)
        
        tk.messagebox.showinfo("Ride Assignment", "Ride assigned!")
        ride_window.destroy()
    except IndexError:
        tk.messagebox.showerror("Error", "Please select a ride to assign.")
    
# Main UI setup
root = tk.Tk()
root.title("Ride Booking System")

label = tk.Label(root, text="Welcome to the Ride Booking System")
label.pack(pady=10)

register_label = tk.Label(root, text="Don't have an account? Register here:")
register_label.pack(pady=5)

username_label = tk.Label(root, text="Enter a new username:")
username_label.pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

password_label = tk.Label(root, text="Enter a password:")
password_label.pack(pady=5)
entry2 = tk.Entry(root, width=30)
entry2.pack(pady=5)

role_label = tk.Label(root, text="Enter role (rider/driver):")
role_label.pack(pady=5)
entry3 = tk.Entry(root, width=30)
entry3.pack(pady=5)

register_button = tk.Button(root, text="Register", command=handle_register)

login_label = tk.Label(root, text="Already have an account? Login here:")
login_label.pack(pady=5)

username_label2 = tk.Label(root, text="Enter your username:")
username_label2.pack(pady=5)
entry4 = tk.Entry(root, width=30)
entry4.pack(pady=5)

password_label2 = tk.Label(root, text="Enter your password:")
password_label2.pack(pady=5)
entry5 = tk.Entry(root, width=30)
entry5.pack(pady=5)

login_button = tk.Button(root, text="Login", command=handle_login)
login_button.pack(pady=5)

root.mainloop()
