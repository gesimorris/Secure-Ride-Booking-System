from Crypto.Cipher import AES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import bcrypt
import json
import os


def pad(data):  # Padding for AES encryption
    return data + ' ' * (16 - len(data) % 16)

def unpad(data):
    return data.rstrip(' ')

def encrypt_ride_data(ride_data, aes_key): # Encrypt ride details using AES
    cipher = AES.new(aes_key, AES.MODE_ECB)  # Simple ECB mode for demonstration
    encrypted_data = cipher.encrypt(pad(ride_data).encode())
    return encrypted_data

def decrypt_ride_data(encrypted_data, aes_key): # Decrypt ride details using AES
    cipher = AES.new(aes_key, AES.MODE_ECB)  # Simple ECB mode for demonstration
    decrypted_data = cipher.decrypt(encrypted_data).decode(errors='ignore')
    return unpad(decrypted_data)
 
    
