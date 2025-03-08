import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, seller, buyer, amount, data):
        """
        Add a new transaction to the list of transactions.
        """
        self.current_transactions.append({
            'seller': seller,
            'buyer': buyer,
            'amount': amount,
            'data': data,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Return the last block in the chain.
        """
        return self.chain[-1]

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.new_transaction("Alice", "Bob", 50, "Anonymized Data")
    blockchain.new_block(proof=12345)
    print("Blockchain:", blockchain.chain)