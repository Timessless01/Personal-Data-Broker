import os
import json
from datetime import datetime
import requests
import random  # For simulating data

class DataCollector:
    def __init__(self):
        self.data = []

    def collect_browser_history(self):
        """
        Simulates browser history data for testing.
        """
        self.data.append({
            "type": "browser_history",
            "url": "https://example.com",
            "title": "Example Website",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def collect_system_data(self):
        """
        Collects basic system data (e.g., OS, CPU, RAM).
        """
        try:
            import platform
            import psutil

            system_data = {
                "type": "system_data",
                "os": platform.system(),
                "os_version": platform.version(),
                "cpu_count": psutil.cpu_count(),
                "total_ram": psutil.virtual_memory().total
            }
            self.data.append(system_data)
        except ImportError:
            # Fallback if psutil is not available
            import platform
            system_data = {
                "type": "system_data",
                "os": platform.system(),
                "os_version": platform.version(),
                "cpu_count": "Unknown",
                "total_ram": "Unknown"
            }
            self.data.append(system_data)
            print("psutil not found. Using fallback system data collection.")
        except Exception as e:
            print(f"Error collecting system data: {e}")

    def collect_location_data(self):
        """
        Collects approximate location data using IP-based geolocation.
        """
        try:
            response = requests.get("https://ipinfo.io")
            location_data = response.json()
            self.data.append({
                "type": "location_data",
                "ip": location_data.get("ip"),
                "city": location_data.get("city"),
                "region": location_data.get("region"),
                "country": location_data.get("country")
            })
        except Exception as e:
            print(f"Error collecting location data: {e}")

    def collect_fitness_data(self):
        """
        Simulates fitness data (e.g., steps, heart rate, sleep hours).
        """
        self.data.append({
            "type": "fitness_data",
            "steps": random.randint(1000, 10000),
            "heart_rate": random.randint(60, 100),
            "sleep_hours": random.randint(4, 8),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def collect_social_media_activity(self):
        """
        Simulates social media activity data.
        """
        self.data.append({
            "type": "social_media_activity",
            "platform": "Twitter",
            "posts": random.randint(1, 10),
            "likes": random.randint(10, 100),
            "shares": random.randint(1, 20),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def collect_ecommerce_data(self):
        """
        Simulates e-commerce purchase history.
        """
        self.data.append({
            "type": "ecommerce_data",
            "platform": "Amazon",
            "purchases": [
                {"item": "Laptop", "price": 1200},
                {"item": "Headphones", "price": 150}
            ],
            "total_spent": 1350,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def save_data(self, filename="user_data.json"):
        """
        Saves collected data to a JSON file.
        """
        try:
            with open(filename, "w") as file:
                json.dump(self.data, file, indent=4)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

# Example usage
if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_browser_history()
    collector.collect_system_data()
    collector.collect_location_data()
    collector.collect_fitness_data()
    collector.collect_social_media_activity()
    collector.collect_ecommerce_data()
    collector.save_data()