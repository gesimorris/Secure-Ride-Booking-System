
Secure Ride Booking App  
By Gesi and Tapiwa

A ride booking system built using Python's Tkinter for the UI.

------------------------------------
Features
------------------------------------

Rider Features
- Book a Ride  
  Input pickup, dropoff, and vehicle type. The system encrypts ride details and signs them with a digital signature. stores the details in the blockchain
- View most recent booking
  Displays ride logs after verifying the digital signature and decrypting the data.
- Logout  
  Returns the user to the main login/register screen.

Driver Features
- Accept Ride Request  
  Accept a ride, putting it in the accepted rides array.
- View accepted rides
  Shows which rides are accepted
- Logout  
  Returns to the login menu.

Installation & Setup

1. Install Python:  
   https://www.python.org/downloads/

2. Install required libraries:
   pip install pycryptodome
   pip install bcrypt
   (Tkinter should be included with python)
   
------------------------------------
How to Use
------------------------------------
Main Menu Options
There are input fields for registration and login. 

Once logged in, users are redirected to a dashboard based on their role (either Rider or Driver).

Rider Menu Options

There are input fields if the rider wants to book a ride, enter each corresponding field
- View most recent rides, press the button

Driver Menu Options

- Accept ride, once clicked new window opens showing available rides. Driver can click accept ride and choose which ride they want
- My rides, once clicked shows the accepted rides from the driver

Security Features

AES Encryption | Encrypts ride details for privacy
RSA Signatures | Ensures the authenticity and integrity of ride data
Hashed passowrd | Ensures password is hashed
Blockchain-like Storage | Encrypted ride data with signatures stored persistently in blockchain_data.json

Files Used

aes.py | AES encryption/decryption for ride details
rsa.py | RSA key generation, encryption & decryption
digital_signature.py | Signing and verifying ride data
blockchain.py | Blockchain-style structure for storing secure ride logs
main.py | Main interface logic using Tkinter
blockchain_data.json | Stores encrypted and signed ride requests
users.json  | Stores user data and hashed passowrd

Note: This UI system opens new windows.
