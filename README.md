Blueprint Analyzer for Material Estimation:
A locally hosted Python application that estimates flooring, drywall, and paint needs based on uploaded blueprints. Users can upload ZIP files containing preprocessed blueprint data, and the app returns per-room material estimates, total usage, and projected waste savings — all displayed through interactive visualizations.

Purpose:
This tool addresses a recurring problem in the construction and remodeling industries: overestimating or underestimating building materials. By automating blueprint analysis and material calculations, the app helps project managers, contractors, and builders make informed, sustainable decisions earlier in the planning process.

Features:
Upload a ZIP file containing a parsed blueprint JSON

Calculates square footage, drywall sheets, paint gallons, and flooring needs

Displays totals and per-room breakdowns

Shows waste reduction insights through charts

All data is processed locally (no internet required)

Project Structure:
Blueprint_Analyzer/

app.py: Flask app to run the web interface

blueprint_parser.py: Core logic for material estimation

requirements.txt: Required Python libraries

templates/index.html: Web dashboard and upload form

Technologies Used:
Python 3

Flask

EasyOCR

OpenCV

NumPy

Chart.js (via HTML template)

Dataset:
This project uses data from the publicly available CubiCasa5K dataset on Kaggle: https://www.kaggle.com/datasets/qmarva/cubicasa5k. For demonstration, blueprint data was pre-parsed into JSON files before upload.

Installation:
Clone or download this repository

Navigate to the project directory in your terminal

Install dependencies using: pip install -r requirements.txt

Running the App:
Activate your virtual environment (optional but recommended)

Run the app using: python app.py

Open your browser and go to http://127.0.0.1:5000

Upload a .zip file containing one parsed JSON file (e.g., 1644.json)

View your results and visualizations in the dashboard

Security and Ethics:
All files are processed locally

No data is transmitted or stored online

Uploaded files are deleted after processing


Notes
Ensure your ZIP file contains a valid .json blueprint file in the correct format

The app has been tested in Mac environment using PyCharm

