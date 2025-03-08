class DataAnonymizer:
    def __init__(self, data):
        self.data = data

    def anonymize_browser_history(self):
        """
        Anonymizes browser history data by removing sensitive URLs.
        """
        for item in self.data:
            if item["type"] == "browser_history":
                item["title"] = "REDACTED"

    def anonymize_system_data(self):
        """
        Anonymizes system data by removing specific details.
        """
        for item in self.data:
            if item["type"] == "system_data":
                item["os_version"] = "REDACTED"

    def anonymize_location_data(self):
        """
        Anonymizes location data by removing the IP address.
        """
        for item in self.data:
            if item["type"] == "location_data":
                item["ip"] = "REDACTED"

    def get_anonymized_data(self):
        """
        Returns the anonymized data.
        """
        return self.data