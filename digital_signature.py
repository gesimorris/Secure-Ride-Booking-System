from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from rsa import encrypt, decrypt
import hashlib


# Sign the message
def sign_message(data, private_key):
    data_hash = hashlib.sha256(data.encode()).hexdigest()
    return encrypt(data_hash, private_key)

def verify_signature(data, signature, public_key):
    expected_hash = hashlib.sha256(data.encode()).hexdigest()
    decrypted_hash = decrypt(signature, public_key)
    return expected_hash == decrypted_hash
