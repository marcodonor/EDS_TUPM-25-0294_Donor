import pandas as pd
import numpy as np
import plotly.express as px
import os

class WindPowerPipeline:
    def __init__(self, file_path):
        self.file_path = file_path
        self.raw_data = None
        self.clean_data = None
        
        # Ensure output directories exist immediately to avoid "Folder Not Found" errors
        if not os.path.exists('data'): os.makedirs('data')
        if not os.path.exists('outputs'): os.makedirs('outputs')

    def ingest_data(self, target_month):
        """Module 1: Data Ingestion with Dynamic Month Filtering"""
        try:
            # Load raw data
            print(f"Reading {self.file_path}...")
            self.raw_data = pd.read_csv(self.file_path)
            
            # Convert Date/Time to actual datetime objects
            # dayfirst=True is used because the format is DD MM YYYY
            self.raw_data['Date/Time'] = pd.to_datetime(self.raw_data['Date/Time'], dayfirst=True)
            
            # Filter data based on user input (1-12)
            self.raw_data = self.raw_data[self.raw_data['Date/Time'].dt.month == target_month] 
            
            if self.raw_data.empty:
                print(f"Warning: No data found for month number {target_month}.")
            else:
                month_name = self.raw_data['Date/Time'].dt.month_name().iloc[0]
                print(f"Successfully filtered data for: {month_name} ({len(self.raw_data)} rows).")
        except Exception as e:
            print(f"CRITICAL ERROR during ingestion: {e}")
            print("Check if the file is open in Excel or if the path is correct.")
            self.raw_data = None

    def clean_data_pipeline(self):
        """Module 2: Automated Cleaning"""
        if self.raw_data is not None and not self.raw_data.empty:
            # Drop missing values and duplicates
            self.clean_data = self.raw_data.dropna().drop_duplicates()
            
            # Ensure the power column is strictly numeric
            self.clean_data['LV ActivePower (kW)'] = pd.to_numeric(self.clean_data['LV ActivePower (kW)'], errors='coerce')
            print("Data cleaning complete.")
        else:
            print("Cleaning skipped: No raw data available.")

    def compute_engineering_stats(self):
        """Module 3: Engineering Data Analytics using NumPy"""
        if self.clean_data is None or self.clean_data.empty:
            return None

        power = self.clean_data['LV ActivePower (kW)'].values
        
        # Calculate Statistics
        stats = {
            "Mean": np.mean(power),
            "Median": np.median(power),
            "StdDev": np.std(power),
            "Variance": np.var(power)
        }
        
        # Calculate Power Curve Deviation if the theoretical column exists
        if 'Theoretical_Power_Curve (KWh)' in self.clean_data.columns:
            self.clean_data['Deviation'] = np.abs(
                self.clean_data['Theoretical_Power_Curve (KWh)'] - self.clean_data['LV ActivePower (kW)']
            )
        return stats

    def generate_visuals(self):
        """Module 4: Visualization (3 Static PNGs and 2 Animated HTMLs)"""
        if self.clean_data is None or self.clean_data.empty:
            return

        m_name = self.clean_data['Date/Time'].dt.month_name().iloc[0]

        # --- STATIC GRAPHS (Minimum: 3) ---
        
        # 1. Power Curve Scatter (Static)
        fig1 = px.scatter(self.clean_data, x='Wind Speed (m/s)', y='LV ActivePower (kW)', 
                          title=f"Power Curve Analysis ({m_name})", template='plotly_dark')
        fig1.write_image("outputs/static_1_power_curve.png")

        # 2. Wind Speed Distribution (Histogram)
        fig2 = px.histogram(self.clean_data, x='Wind Speed (m/s)', nbins=50,
                            title=f"Wind Speed Frequency Distribution ({m_name})", color_discrete_sequence=['#00CC96'])
        fig2.write_image("outputs/static_2_wind_dist.png")

        # 3. Power Deviation Spread (Boxplot)
        if 'Deviation' in self.clean_data.columns:
            fig3 = px.box(self.clean_data, y='Deviation', title=f"Statistical Spread of Power Deviation ({m_name})")
            fig3.write_image("outputs/static_3_deviation_boxplot.png")

        # --- ANIMATED GRAPHS (Minimum: 2) ---
        
        # Sort data for chronological animations
        anim_df = self.clean_data.sort_values('Date/Time').head(1500)

        # 1. Temporal Power Trend (Animation)
        fig_anim1 = px.scatter(anim_df, x="Wind Speed (m/s)", y="LV ActivePower (kW)", 
                               animation_frame=anim_df['Date/Time'].dt.strftime('%d %H:%M'), 
                               range_y=[0, 4500], title=f"Dynamic Power Trend: {m_name}")
        fig_anim1.write_html("outputs/animation_1_trend.html")

        # 2. Distribution Shift Animation (Showing spread changes over the month)
        fig_anim2 = px.histogram(anim_df, x="LV ActivePower (kW)", 
                                 animation_frame=anim_df['Date/Time'].dt.day,
                                 range_x=[0, 4000], range_y=[0, 50],
                                 title=f"Daily Power Distribution Shift: {m_name}")
        fig_anim2.write_html("outputs/animation_2_distribution.html")

        print(f"All 5 required visuals saved to 'outputs/' for {m_name}.")

    def save_results(self):
        """Module 5: Exporting Cleaned Data"""
        if self.clean_data is not None:
            self.clean_data.to_csv("data/dataset_cleaned.csv", index=False)
            print("Cleaned dataset saved to 'data/dataset_cleaned.csv'.")

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    # Make sure T1.csv is in the same folder as this script
    FILE_NAME = "data/T1.csv" 
    
    try:
        val = input("Enter the month number to analyze (1 for Jan, 2 for Feb, etc.): ")
        user_month = int(val)
        
        if not 1 <= user_month <= 12:
            print("Error: Please enter a number between 1 and 12.")
        else:
            # Initialize the pipeline
            pipeline = WindPowerPipeline(FILE_NAME)
            
            # Step 1: Ingest
            pipeline.ingest_data(target_month=user_month)
            
            # Step 2: Clean and Process (only if ingestion worked)
            if pipeline.raw_data is not None and not pipeline.raw_data.empty:
                pipeline.clean_data_pipeline()
                
                # Step 3: Analytics
                results = pipeline.compute_engineering_stats()
                
                if results:
                    print("-" * 30)
                    print("ENGINEERING STATISTICS")
                    for key, value in results.items():
                        print(f"{key}: {value:.2f}")
                    print("-" * 30)
                    
                    # Step 4: Visuals & Storage
                    pipeline.generate_visuals()
                    pipeline.save_results()
                    print("\nPipeline execution finished successfully!")
            else:
                print("Pipeline halted due to data issues.")
                
    except ValueError:
        print("Invalid input. Please enter a numeric value for the month.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")