# Spreadsheet Analytics Platform

A Flask-based web application that allows users to upload Excel spreadsheets, generate statistical analyses, visualize data with charts, and export analysis reports as PDFs.

## Features

* Upload Excel (.xlsx) datasets
* View dataset overview and column information
* Preview uploaded spreadsheet data
* Generate histograms for numeric columns
* Generate scatter plots between two numeric columns
* Calculate descriptive statistics:
  * Mean
  * Median
  * Standard Deviation
  * Missing Values
* Calculate correlation coefficients for scatter plots
* Generate downloadable PDF analysis reports
* Session-based user isolation for multi-user support
* Error handling for invalid files and analysis requests

## Technologies Used

### Backend

* Python
* Flask
* Pandas

### Data Visualization

* Matplotlib

### Spreadsheet Processing

* OpenPyXL

### PDF Generation

* ReportLab

### Frontend

* HTML
* CSS
* Jinja2 Templates

## Project Structure

spreadsheet-site/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── home.html
│   ├── overview.html
│   ├── analysis.html
│   └── error.html
│
├── static/
│   └── plots/
│
├── uploads/
└── reports/

## Installation

Clone the repository:

git clone <repository-url>
cd spreadsheet-site

Install dependencies:

pip install -r requirements.txt

Set a secret key:

### Windows PowerShell

$env:SECRET_KEY="your-secret-key"

### Linux / macOS

export SECRET_KEY="your-secret-key"

Run the application:

python app.py

Open:

http://127.0.0.1:5000

in your browser.

## Usage

1. Upload an Excel spreadsheet (.xlsx).
2. Review dataset information and preview rows.
3. Select a visualization type:
   * Histogram
   * Scatter Plot
4. Choose the relevant columns.
5. Generate the analysis.
6. Download a PDF report containing the generated results.

## Future Improvements

* Support CSV files
* Additional chart types
* Correlation heatmaps
* Regression analysis
* User authentication
* Cloud file storage
* Interactive visualizations with Plotly
* Dataset summary reports

## Deployment

The application is designed to be deployed using Render with environment-variable-based configuration for secure session management.

## Author

Abhirag Bodi
