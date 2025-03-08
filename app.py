import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import json
from data_collection import DataCollector
from data_anonymization import DataAnonymizer
from marketplace import Marketplace
from notifications import send_email
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database initialization
def init_db():
    conn = sqlite3.connect("personal_data_broker.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    """)

    # Create companies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buyer TEXT NOT NULL,
            seller TEXT NOT NULL,
            amount REAL NOT NULL,
            data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create subscriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            plan TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
    """)

    conn.commit()
    conn.close()


class PersonalDataBrokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Data Broker")
        self.root.geometry("600x400")

        # Initialize database
        init_db()

        # Initialize marketplace
        self.marketplace = Marketplace()

        # Current user (None if not logged in)
        self.current_user = None
        self.current_user_email = None  # Track user's email for notifications

        # Create UI elements
        self.label = tk.Label(root, text="Welcome to Personal Data Broker!", font=("Arial", 16))
        self.label.pack(pady=20)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.signup_button = tk.Button(root, text="Signup", command=self.signup)
        self.signup_button.pack(pady=10)

        self.company_signup_button = tk.Button(root, text="Company Signup", command=self.company_signup)
        self.company_signup_button.pack(pady=10)

    def login(self):
        """
        Handles user login.
        """
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show="*")

        if username and password:
            conn = sqlite3.connect("personal_data_broker.db")
            cursor = conn.cursor()

            # Check if the user exists
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                self.current_user = username
                self.current_user_email = user[3]  # Store user's email
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

            conn.close()

    def signup(self):
        """
        Handles user signup.
        """
        username = simpledialog.askstring("Signup", "Choose a username:")
        password = simpledialog.askstring("Signup", "Choose a password:", show="*")
        email = simpledialog.askstring("Signup", "Enter your email:")

        if username and password and email:
            conn = sqlite3.connect("personal_data_broker.db")
            cursor = conn.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
            else:
                # Insert new user
                cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
                conn.commit()
                messagebox.showinfo("Success", "Signup successful! Please login.")
                self.current_user = username
                self.current_user_email = email
                self.show_main_menu()

                # Send email notification after signup
                try:
                    send_email(
                        to=email,
                        subject="Welcome to Personal Data Broker",
                        body=f"Hi {username},\n\nThank you for signing up with Personal Data Broker!"
                    )
                except Exception as e:
                    print(f"Failed to send email: {e}")

            conn.close()

    def company_signup(self):
        """
        Handles company signup.
        """
        name = simpledialog.askstring("Company Signup", "Enter your company name:")
        password = simpledialog.askstring("Company Signup", "Choose a password:", show="*")

        if name and password:
            conn = sqlite3.connect("personal_data_broker.db")
            cursor = conn.cursor()

            # Check if the company already exists
            cursor.execute("SELECT * FROM companies WHERE name = ?", (name,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Company already exists.")
            else:
                # Insert new company
                cursor.execute("INSERT INTO companies (name, password) VALUES (?, ?)", (name, password))
                conn.commit()
                messagebox.showinfo("Success", "Company registration successful!")

            conn.close()

    def show_main_menu(self):
        """
        Displays the main menu after login.
        """
        # Clear the login/signup buttons
        self.login_button.pack_forget()
        self.signup_button.pack_forget()
        self.company_signup_button.pack_forget()

        # Add main menu buttons
        self.collect_button = tk.Button(self.root, text="Collect Data", command=self.collect_data)
        self.collect_button.pack(pady=10)

        self.list_button = tk.Button(self.root, text="List Data for Sale", command=self.list_data)
        self.list_button.pack(pady=10)

        self.view_listings_button = tk.Button(self.root, text="View Listings", command=self.view_listings)
        self.view_listings_button.pack(pady=10)

        self.buy_button = tk.Button(self.root, text="Buy Data", command=self.buy_data)
        self.buy_button.pack(pady=10)

        self.view_blockchain_button = tk.Button(self.root, text="View Blockchain", command=self.view_blockchain)
        self.view_blockchain_button.pack(pady=10)

        self.earnings_label = tk.Label(self.root, text="Earnings: $0", font=("Arial", 14))
        self.earnings_label.pack(pady=20)

        self.dashboard_button = tk.Button(self.root, text="User Dashboard", command=self.show_user_dashboard)
        self.dashboard_button.pack(pady=10)

        self.profile_button = tk.Button(self.root, text="User Profile", command=self.show_user_profile)
        self.profile_button.pack(pady=10)

        self.subscription_button = tk.Button(self.root, text="Manage Subscriptions", command=self.manage_subscriptions)
        self.subscription_button.pack(pady=10)

        self.notifications_button = tk.Button(self.root, text="Notifications", command=self.show_notifications)
        self.notifications_button.pack(pady=10)

    def collect_data(self):
        """
        Collects user data and saves it to a file.
        """
        collector = DataCollector()
        collector.collect_browser_history()
        collector.collect_system_data()
        collector.collect_location_data()
        collector.collect_fitness_data()
        collector.collect_social_media_activity()
        collector.collect_ecommerce_data()
        collector.save_data()
        messagebox.showinfo("Success", "Data collected and saved to user_data.json!")

    def list_data(self):
        """
        Lists anonymized data for sale.
        """
        try:
            with open("user_data.json", "r") as file:
                data = json.load(file)
            anonymizer = DataAnonymizer(data)
            anonymizer.anonymize_browser_history()
            anonymizer.anonymize_system_data()
            anonymizer.anonymize_location_data()
            with open("anonymized_data.json", "w") as file:
                json.dump(anonymizer.get_anonymized_data(), file, indent=4)

            price = simpledialog.askfloat("Set Price", "Enter the price for your data:")
            if price:
                self.marketplace.list_data(anonymizer.get_anonymized_data(), price)
                messagebox.showinfo("Success", "Data listed for sale!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def view_listings(self):
        """
        Displays all current listings.
        """
        listings_window = tk.Toplevel(self.root)
        listings_window.title("Listings")
        listings_window.geometry("500x300")

        listings_text = tk.Text(listings_window, wrap=tk.WORD)
        listings_text.pack(fill=tk.BOTH, expand=True)

        for i, listing in enumerate(self.marketplace.listings):
            listings_text.insert(tk.END, f"Listing {i+1}:\n")
            listings_text.insert(tk.END, f"Data: {json.dumps(listing['data'], indent=2)}\n")
            listings_text.insert(tk.END, f"Price: ${listing['price']}\n")
            listings_text.insert(tk.END, "-" * 40 + "\n")

    def buy_data(self):
        """
        Buys data and records the transaction on the blockchain.
        """
        if not self.marketplace.listings:
            messagebox.showinfo("Info", "No listings available to buy.")
            return

        # Display listings
        listings_window = tk.Toplevel(self.root)
        listings_window.title("Available Listings")
        listings_window.geometry("500x300")

        listings_text = tk.Text(listings_window, wrap=tk.WORD)
        listings_text.pack(fill=tk.BOTH, expand=True)

        for i, listing in enumerate(self.marketplace.listings):
            listings_text.insert(tk.END, f"Listing {i+1}:\n")
            listings_text.insert(tk.END, f"Data: {json.dumps(listing['data'], indent=2)}\n")
            listings_text.insert(tk.END, f"Price: ${listing['price']}\n")
            listings_text.insert(tk.END, "-" * 40 + "\n")

        # Ask for listing number
        def on_buy():
            try:
                listing_index = int(listing_number_entry.get()) - 1
                if listing_index < 0 or listing_index >= len(self.marketplace.listings):
                    messagebox.showerror("Error", "Invalid listing number.")
                    return

                # Simulate payment
                payment_confirmed = messagebox.askyesno("Confirm Payment", "Do you want to proceed with the payment?")
                if payment_confirmed:
                    buyer = simpledialog.askstring("Buy Data", "Enter your name:")
                    if buyer:
                        # Record transaction and remove data from marketplace
                        self.marketplace.buy_data(listing_index, buyer)
                        self.marketplace.listings.pop(listing_index)  # Remove purchased data
                        self.update_earnings()
                        messagebox.showinfo("Success", "Data purchased and transaction recorded on the blockchain!")
                        listings_window.destroy()

                        # Send email notification after purchase
                        try:
                            send_email(
                                to=self.current_user_email,
                                subject="Purchase Confirmation",
                                body=f"Hi {buyer},\n\nYour purchase was successful! Thank you for using Personal Data Broker."
                            )
                        except Exception as e:
                            print(f"Failed to send email: {e}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        # Add an entry field for the listing number
        listing_number_frame = tk.Frame(listings_window)
        listing_number_frame.pack(pady=10)

        tk.Label(listing_number_frame, text="Enter Listing Number:").pack(side=tk.LEFT)
        listing_number_entry = tk.Entry(listing_number_frame)
        listing_number_entry.pack(side=tk.LEFT, padx=10)

        buy_button = tk.Button(listing_number_frame, text="Buy", command=on_buy)
        buy_button.pack(side=tk.LEFT)

    def view_blockchain(self):
        """
        Displays the entire blockchain.
        """
        blockchain_window = tk.Toplevel(self.root)
        blockchain_window.title("Blockchain")
        blockchain_window.geometry("500x300")

        blockchain_text = tk.Text(blockchain_window, wrap=tk.WORD)
        blockchain_text.pack(fill=tk.BOTH, expand=True)

        for block in self.marketplace.blockchain.chain:
            blockchain_text.insert(tk.END, json.dumps(block, indent=2) + "\n")
            blockchain_text.insert(tk.END, "-" * 40 + "\n")

    def update_earnings(self):
        """
        Updates the user's earnings based on blockchain transactions.
        """
        earnings = 0
        for block in self.marketplace.blockchain.chain:
            for transaction in block["transactions"]:
                if transaction["seller"] == "User":
                    earnings += transaction["amount"]
        self.earnings_label.config(text=f"Earnings: ${earnings}")

    def show_user_dashboard(self):
        """
        Displays the user dashboard with earnings and transaction history.
        """
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("User Dashboard")
        dashboard_window.geometry("600x400")

        # Fetch and display user data
        tk.Label(dashboard_window, text=f"Welcome, {self.current_user}!", font=("Arial", 16)).pack(pady=20)
        tk.Label(dashboard_window, text="Earnings: $0", font=("Arial", 14)).pack(pady=10)
        tk.Button(dashboard_window, text="View Transactions", command=self.view_transactions).pack(pady=10)

    def show_user_profile(self):
        """
        Displays the user profile window.
        """
        profile_window = tk.Toplevel(self.root)
        profile_window.title("User Profile")
        profile_window.geometry("400x300")

        tk.Label(profile_window, text=f"Username: {self.current_user}", font=("Arial", 14)).pack(pady=20)
        tk.Label(profile_window, text=f"Email: {self.current_user_email}", font=("Arial", 14)).pack(pady=10)
        tk.Button(profile_window, text="Edit Profile", command=self.edit_profile).pack(pady=10)

    def edit_profile(self):
        """
        Allows the user to edit their profile.
        """
        new_username = simpledialog.askstring("Edit Profile", "Enter new username:")
        new_email = simpledialog.askstring("Edit Profile", "Enter new email:")

        if new_username or new_email:
            conn = sqlite3.connect("personal_data_broker.db")
            cursor = conn.cursor()

            if new_username:
                cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, self.current_user))
                self.current_user = new_username
            if new_email:
                cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, self.current_user))
                self.current_user_email = new_email

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Profile updated successfully!")

    def show_notifications(self):
        """
        Displays notifications for new listings or purchases.
        """
        notifications_window = tk.Toplevel(self.root)
        notifications_window.title("Notifications")
        notifications_window.geometry("400x300")

        notifications_text = tk.Text(notifications_window, wrap=tk.WORD)
        notifications_text.pack(fill=tk.BOTH, expand=True)

        # Example notifications
        notifications_text.insert(tk.END, "No new notifications.\n")

    def visualize_earnings(self):
        """
        Displays a chart of the user's earnings over time.
        """
        earnings_data = [100, 150, 200, 250, 300]  # Example data
        fig, ax = plt.subplots()
        ax.plot(earnings_data, marker='o')
        ax.set_title("Earnings Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Earnings ($)")

        # Embed the chart in the Tkinter window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Earnings Visualization")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def manage_subscriptions(self):
        """
        Manages company subscriptions.
        """
        subscription_window = tk.Toplevel(self.root)
        subscription_window.title("Manage Subscriptions")
        subscription_window.geometry("500x300")

        tk.Label(subscription_window, text="Subscription Management", font=("Arial", 14)).pack(pady=10)

        tk.Button(subscription_window, text="Add Subscription", command=self.add_subscription).pack(pady=10)
        tk.Button(subscription_window, text="View Subscriptions", command=self.view_subscriptions).pack(pady=10)

    def add_subscription(self):
        """
        Adds a new subscription for a company.
        """
        company_id = simpledialog.askstring("Add Subscription", "Enter Company ID:")
        plan = simpledialog.askstring("Add Subscription", "Enter Plan Name:")
        start_date = simpledialog.askstring("Add Subscription", "Enter Start Date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Add Subscription", "Enter End Date (YYYY-MM-DD):")

        if company_id and plan and start_date and end_date:
            conn = sqlite3.connect("personal_data_broker.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO subscriptions (company_id, plan, start_date, end_date)
                VALUES (?, ?, ?, ?)
            """, (company_id, plan, start_date, end_date))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Subscription added successfully!")

    def view_subscriptions(self):
        """
        Displays all subscriptions.
        """
        conn = sqlite3.connect("personal_data_broker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM subscriptions")
        subscriptions = cursor.fetchall()

        subscriptions_window = tk.Toplevel(self.root)
        subscriptions_window.title("Subscriptions")
        subscriptions_window.geometry("500x300")

        subscriptions_text = tk.Text(subscriptions_window, wrap=tk.WORD)
        subscriptions_text.pack(fill=tk.BOTH, expand=True)

        for subscription in subscriptions:
            subscriptions_text.insert(tk.END, f"ID: {subscription[0]}\n")
            subscriptions_text.insert(tk.END, f"Company ID: {subscription[1]}\n")
            subscriptions_text.insert(tk.END, f"Plan: {subscription[2]}\n")
            subscriptions_text.insert(tk.END, f"Start Date: {subscription[3]}\n")
            subscriptions_text.insert(tk.END, f"End Date: {subscription[4]}\n")
            subscriptions_text.insert(tk.END, "-" * 40 + "\n")

        conn.close()

    def view_transactions(self):
        """
        Displays the user's transaction history.
        """
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transaction History")
        transactions_window.geometry("500x300")

        transactions_text = tk.Text(transactions_window, wrap=tk.WORD)
        transactions_text.pack(fill=tk.BOTH, expand=True)

        for block in self.marketplace.blockchain.chain:
            for transaction in block["transactions"]:
                if transaction["buyer"] == self.current_user or transaction["seller"] == self.current_user:
                    transactions_text.insert(tk.END, f"Transaction ID: {transaction['id']}\n")
                    transactions_text.insert(tk.END, f"Buyer: {transaction['buyer']}\n")
                    transactions_text.insert(tk.END, f"Seller: {transaction['seller']}\n")
                    transactions_text.insert(tk.END, f"Amount: ${transaction['amount']}\n")
                    transactions_text.insert(tk.END, f"Data: {transaction['data']}\n")
                    transactions_text.insert(tk.END, "-" * 40 + "\n")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalDataBrokerApp(root)
    root.mainloop()