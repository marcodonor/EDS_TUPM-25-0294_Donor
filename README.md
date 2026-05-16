# Computer Programming 1 Final Project: Wind Turbine Power Curve Analytics (REN-01)

# Project Overview
This is my final project for Computer Programming 1. It is a Python-based data pipeline built using Object-Oriented Programming (OOP) to automatically load, clean, analyze, and graph a real-world SCADA dataset from a wind turbine. 

The main goal of the code is to calculate how much power the turbine is losing (power curve deviation) compared to what the manufacturer promised in their manual. The pipeline filters the data down to a unique month so we can see exactly where the turbine underperforms due to things like blade wear, mechanical friction, or control errors, without having to sift through giant spreadsheets manually.

# Repository Structure
Following the submission guidelines, my repository is organized into this exact folder structure:
├── main.py                  1. The main Python script containing the code class
├── requirements.txt         2. List of libraries needed to run the project
├── data/                    3. Folder for our datasets
│   ├── dataset_original.csv 4. The raw, untouched SCADA data file
│   └── dataset_cleaned.csv  5. The clean data file saved by our program
└── outputs/                 6. Folder where the code saves all the plots
    ├── static_1_power_curve.png     7. Scatter plot of wind speed vs power output
    ├── static_2_wind_dist.png       8. Histogram showing how often different wind speeds occur
    ├── static_3_deviation_boxplot.png  9. Boxplot showing the spread of power losses
    ├── animation_1_trend.html       10. Animated scatter plot showing changes day-by-day
    └── animation_2_distribution.html 11. Animated histogram showing daily frequency shifts

# How the Code Works
Everything is built inside a single Python class called `WindPowerPipeline` and split into 5 clear steps:
1. Data Ingestion: Loads the CSV file and asks the user to type in a month so the data slice is completely unique.
2. Data Cleaning: Automatically handles missing data, converts column types into floats so they don't break, and drops any rows with blank (`NaN`) fields.
3. NumPy Analytics: Uses vectorized NumPy math (no slow `for` loops) to instantly find the mean, standard deviation, and variance, plus the exact power drop (`Delta P`) for all 1,440 rows.
4. Visualization: Creates 3 static charts using Matplotlib and 2 interactive HTML animations using Plotly to show trends over time.
5. File Export: Checks your folders and safely saves the cleaned CSV data and the generated plots into the right directories.

# Requirements & Setup
This project runs on Python 3.8+ and needs a few external libraries to work. To set up your computer and install everything automatically, open your terminal in this folder and run:

run this in terminal first:
pip install -r requirements.txt