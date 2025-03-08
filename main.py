import json  # Add this import
from data_collection import DataCollector
from data_anonymization import DataAnonymizer
from marketplace import Marketplace

def main():
    print("Welcome to Personal Data Broker!")
    print("1. Collect Data")
    print("2. List Data for Sale")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # Collect data
        collector = DataCollector()
        collector.collect_browser_history()
        collector.collect_system_data()
        collector.collect_location_data()
        collector.save_data()
        print("Data collected and saved to user_data.json.")

    elif choice == "2":
        # List data for sale
        with open("user_data.json", "r") as file:
            data = json.load(file)
        anonymizer = DataAnonymizer(data)
        anonymizer.anonymize_browser_history()
        anonymizer.anonymize_system_data()
        anonymizer.anonymize_location_data()
        with open("anonymized_data.json", "w") as file:
            json.dump(anonymizer.get_anonymized_data(), file, indent=4)

        marketplace = Marketplace()
        price = float(input("Enter the price for your data (e.g., 50): "))
        marketplace.list_data(anonymizer.get_anonymized_data(), price)
        marketplace.view_listings()

    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()