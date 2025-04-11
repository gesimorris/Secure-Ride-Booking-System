
import hashlib
import json
from time import time
import os

class Blockchain:
    def __init__(self, filename='blockchain_data.json'):
        self.chain = []
        self.filename = filename
        self.load_chain()

        if not self.chain:
            self.new_block(previous_hash='1', proof=100)

    def new_ride(self, rider, driver, origin, destination):
        self.current_rides.append({
            'rider': rider,
            'driver': driver,
            'origin': origin,
            'destination': destination,
            'timestamp': time(),
        })
        return self.last_block['index'] + 1

    def add_transaction(self, encrypted_data, signature, rider_public_key):
        transaction = {
            'ride_data': encrypted_data.hex(),
            'signature': signature,
            'rider_public_key': rider_public_key,
            
        }
        self.chain.append(transaction)
        self.save_chain()
    

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'rides': getattr(self, 'current_rides', []),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else '1',
        }
        self.current_rides = []
        self.chain.append(block)
        self.save_chain()
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def save_chain(self):
        with open(self.filename, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def load_chain(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.chain = json.load(f)
        else:
            self.chain = []

    def get_chain(self):
        return json.dumps(self.chain, indent=4)
