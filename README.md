# Banking-Data-Analysis-and-Reporting
Python script to process and analyze simulated banking document data extracted with OCR, identifying and correcting errors, reconciling transactions, and detecting any anomalies.

# Overview
This script performs data cleaning, analysis, reconciliation, anomaly detection, and generates a PDF report summarizing the findings. It processes banking transaction data from a CSV file, cleans the data, analyzes individual transactions and aggregated totals, detects anomalies, and visualizes transaction data.

# Requirements
Python 3.x
Pandas
Matplotlib
Seaborn
ReportLab

# How to Run
1. Clone or download the repository to your local machine.
2. Place your banking data CSV file in the same directory as the script.
3. Install the required libraries using pip:
   pip install pandas matplotlib seaborn reportlab
4. Open a terminal or command prompt in the directory containing the script.
5. Run the script:
   python banking_data_analysis.py
6. After execution, a PDF report named banking_data_analysis_report.pdf will be generated in the same directory.

# Approach

# Data Cleaning:
Correct OCR-like errors in account numbers.
Normalize amount values.
Fill missing values in transaction types.
# Analysis:
Separate individual transactions from aggregated data.
Calculate total amounts for individual and aggregated transactions.
Check reconciliation status between individual and aggregated totals.
# Anomaly Detection:
Define anomalies as transactions with amounts greater than a specified threshold.
List detected anomalies in the report.
# Visualization:
Generate a pie chart showing the distribution of transaction types.
# Report Generation:
Create a PDF report summarizing reconciliation status, total amounts, detected anomalies, and recommendations.
# Interpretation of Output
Reconciliation Status: Indicates whether the reconciliation between individual and aggregated totals was successful or failed.
Total Individual Transactions Amount: Sum of amounts for individual transactions.
Aggregated Total Amount: Sum of amounts for aggregated transactions.
Detected Anomalies: Lists the indices, descriptions, and amounts of detected anomalies.
Recommendations: Provides recommendations for data analysis and quality control.
