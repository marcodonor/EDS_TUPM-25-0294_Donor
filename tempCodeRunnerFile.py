clean_data['LV ActivePower (kW)'], errors='coerce')
            print("Data cleaning complete.")
        else:
            print("Cleaning skipped: No raw data available.")

    def compute_engineering_stats(self):