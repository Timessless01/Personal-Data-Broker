import sqlite3
import json
from blockchain import Blockchain

class Marketplace:
    def __init__(self, db_name="personal_data_broker.db"):
        """
        Initializes the Marketplace with a SQLite database and a blockchain.
        """
        self.blockchain = Blockchain()  # Initialize blockchain
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_database()  # Ensure the database schema is set up

    def _initialize_database(self):
        """
        Creates the necessary tables in the database if they don't already exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                data TEXT NOT NULL,
                price REAL NOT NULL,
                seller TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def list_data(self, data, price, seller):
        """
        Lists anonymized data for sale in the database.
        """
        try:
            self.cursor.execute("""
                INSERT INTO listings (type, data, price, seller)
                VALUES (?, ?, ?, ?)
            """, (data["type"], json.dumps(data), price, seller))
            self.conn.commit()
            print("Data listed for sale!")
        except sqlite3.Error as e:
            print(f"Error listing data: {e}")

    def buy_data(self, listing_id, buyer):
        """
        Buys data and records the transaction on the blockchain.
        """
        try:
            # Fetch the listing from the database
            self.cursor.execute("SELECT * FROM listings WHERE id = ?", (listing_id,))
            listing = self.cursor.fetchone()

            if not listing:
                print("Invalid listing ID.")
                return

            # Record the transaction on the blockchain
            self.blockchain.new_transaction(listing[4], buyer, listing[3], listing[2])
            self.blockchain.new_block(proof=12345)  # Add a new block to the chain

            # Remove the purchased data from the listings table
            self.cursor.execute("DELETE FROM listings WHERE id = ?", (listing_id,))
            self.conn.commit()

            print(f"Data purchased by {buyer} for ${listing[3]}. Transaction recorded on the blockchain.")
        except sqlite3.Error as e:
            print(f"Error buying data: {e}")

    def view_listings(self):
        """
        Displays all current listings.
        """
        try:
            self.cursor.execute("SELECT * FROM listings")
            listings = self.cursor.fetchall()

            if not listings:
                print("No listings available.")
            else:
                for listing in listings:
                    print(f"Listing ID: {listing[0]}")
                    print(f"Type: {listing[1]}")
                    print(f"Data: {json.loads(listing[2])}")  # Deserialize JSON data
                    print(f"Price: ${listing[3]}")
                    print(f"Seller: {listing[4]}")
                    print("-" * 40)
        except sqlite3.Error as e:
            print(f"Error fetching listings: {e}")

    def view_blockchain(self):
        """
        Displays the entire blockchain.
        """
        print("Blockchain Transactions:")
        for block in self.blockchain.chain:
            print(json.dumps(block, indent=2))
            print("-" * 40)

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()

# Example usage
if __name__ == "__main__":
    marketplace = Marketplace()

    # List some data for sale
    marketplace.list_data(
        {"type": "browser_history", "url": "https://example.com"},
        price=50,
        seller="User123"
    )

    # View all listings
    marketplace.view_listings()

    # Buy data (replace 1 with a valid listing ID from your database)
    marketplace.buy_data(1, buyer="CompanyXYZ")

    # View the blockchain
    marketplace.view_blockchain()

    # Close the database connection
    marketplace.close()