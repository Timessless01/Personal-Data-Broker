import analytics
from marketplace import Marketplace

def display_dashboard():
    print("Welcome to the Personal Data Broker Dashboard")
    print("1. Show Analytics")
    print("2. View Earnings")
    print("3. View Listed Data")
    print("4. View Transaction History")
    print("5. Exit")

    marketplace = Marketplace()

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            analytics.show_analytics()
        elif choice == "2":
            view_earnings(marketplace)
        elif choice == "3":
            view_listed_data(marketplace)
        elif choice == "4":
            view_transaction_history(marketplace)
        elif choice == "5":
            print("Exiting the dashboard.")
            break
        else:
            print("Invalid choice. Please try again.")

def view_earnings(marketplace):
    """
    Displays the user's earnings.
    """
    earnings = 0
    for block in marketplace.blockchain.chain:
        for transaction in block["transactions"]:
            if transaction["seller"] == "User":
                earnings += transaction["amount"]
    print(f"Your total earnings: ${earnings}")

def view_listed_data(marketplace):
    """
    Displays all listed data from the database.
    """
    marketplace.cursor.execute("SELECT * FROM listings")
    listings = marketplace.cursor.fetchall()

    if not listings:
        print("No data listed for sale.")
    else:
        for listing in listings:
            print(f"Listing ID: {listing[0]}")
            print(f"Type: {listing[1]}")
            print(f"Data: {listing[2]}")
            print(f"Price: ${listing[3]}")
            print(f"Seller: {listing[4]}")
            print("-" * 40)

def view_transaction_history(marketplace):
    """
    Displays the transaction history.
    """
    if not marketplace.blockchain.chain:
        print("No transactions recorded.")
    else:
        print("Transaction History:")
        for block in marketplace.blockchain.chain:
            for transaction in block["transactions"]:
                print(f"Seller: {transaction['seller']}")
                print(f"Buyer: {transaction['buyer']}")
                print(f"Amount: ${transaction['amount']}")
                print(f"Data: {transaction['data']}")
                print("-" * 40)

if __name__ == "__main__":
    display_dashboard()