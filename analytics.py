import matplotlib.pyplot as plt
import sqlite3

def show_analytics():
    """
    Displays data analytics by showing a bar chart of the number of listings grouped by data type.
    """
    # Fetch data from the database
    conn = sqlite3.connect("personal_data_broker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT type, COUNT(*) FROM listings GROUP BY type")
    data = cursor.fetchall()
    conn.close()

    # Plot the data
    types = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.bar(types, counts)
    plt.xlabel("Data Type")
    plt.ylabel("Number of Listings")
    plt.title("Data Listings by Type")
    plt.show()

def show_earnings_over_time(marketplace):
    """
    Displays a line chart of earnings over time based on transactions in the marketplace blockchain.

    Args:
        marketplace: An object representing the marketplace, which contains a blockchain attribute.
    """
    timestamps = []
    earnings = []
    total = 0

    # Iterate through the blockchain to calculate cumulative earnings
    for block in marketplace.blockchain.chain:
        for transaction in block["transactions"]:
            if transaction["seller"] == "User":
                total += transaction["amount"]
                timestamps.append(block["timestamp"])
                earnings.append(total)

    # Plot the data
    plt.plot(timestamps, earnings)
    plt.xlabel("Time")
    plt.ylabel("Earnings ($)")
    plt.title("Earnings Over Time")
    plt.show()

# Example usage (commented out for now)
# if __name__ == "__main__":
#     show_analytics()
#     # Assuming `marketplace` is an object with a blockchain attribute
#     # show_earnings_over_time(marketplace)