import pandas as pd
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.utils import ImageReader  # Import ImageReader

# Load the CSV file
df = pd.read_csv('banking_data_assignment.csv')

# Correct OCR-like errors in account numbers
df.loc[df['Account Number'].str.startswith('ACC'), 'Account Number'] = df.loc[
    df['Account Number'].str.startswith('ACC'), 'Account Number'].str.replace('O', '0')

# Normalize amount values
df['Amount'] = df['Amount'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Check and fill missing values in the 'Transaction Type' column
df['Transaction Type'] = df['Transaction Type'].fillna('')

# Identify positive values for withdrawals and make them negative
withdrawal_mask = ((df['Transaction Type'] == 'Withdrawal') | 
                   (df['Transaction Type'] == 'ATM Withdrawal')) & (df['Amount'] > 0)
df.loc[withdrawal_mask, 'Amount'] *= -1

def clean_description(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s-]', '', text)
    return text

df['Description'] = df['Description'].apply(clean_description)

# Save cleaned data to a new CSV file
df.to_csv('cleaned_bank_transactions.csv', index=False)

# Load the cleaned CSV file
cleaned_df = pd.read_csv('cleaned_bank_transactions.csv')

# Filter out 'SUBTOTAL' and 'YEARLY TOTAL' rows
individual_transactions = cleaned_df[~cleaned_df['Account Number'].str.contains('TOTAL')]

# Calculate total amount for individual transactions
total_individual_amount = individual_transactions['Amount'].sum()

# Check if 'YEARLY TOTAL' exists in the 'Account Number' column
if 'YEARLY TOTAL' in cleaned_df['Account Number'].values:
    # Calculate aggregated total amount excluding 'SUBTOTAL' rows
    aggregated_total_amount = cleaned_df.loc[
        (cleaned_df['Account Number'] == 'YEARLY TOTAL') & 
        (~cleaned_df['Account Number'].str.contains('SUBTOTAL')), 'Amount'].sum()
    reconciliation_status = "Reconciliation Successful" if total_individual_amount == aggregated_total_amount else "Reconciliation Failed"
else:
    aggregated_total_amount = 0
    reconciliation_status = "Reconciliation Failed - 'YEARLY TOTAL' not found"

# Data Visualization
plt.figure(figsize=(12, 6))

# Pie chart of transaction types
plt.subplot(1, 2, 2)
transaction_type_counts = individual_transactions['Transaction Type'].value_counts()
plt.pie(transaction_type_counts, labels=transaction_type_counts.index, autopct='%1.1f%%')
plt.title('Distribution of Transaction Types')

plt.tight_layout()

# Print reconciliation status and totals
print("Reconciliation Status:", reconciliation_status)
print("Total Individual Transactions Amount:", total_individual_amount)
print("Aggregated Total Amount:", aggregated_total_amount)

# Save the generated plots as bytes
buffer = BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Create PDF and add report content
c = canvas.Canvas("banking_data_analysis_report.pdf", pagesize=letter)

# Set font size and style for the main heading
c.setFont("Helvetica-Bold", 16)

# Add main heading
main_heading = "Banking Data Analysis Report"
heading_width = c.stringWidth(main_heading, "Helvetica-Bold")  # Get width to center the heading
c.drawString((letter[0] - heading_width) / 2, 750, main_heading)

# Set font size and style for other content
c.setFont("Helvetica", 12)

# Add other content
c.drawString(100, 730, f"Reconciliation Status: {reconciliation_status}")
c.drawString(100, 710, f"Total Individual Transactions Amount: {total_individual_amount:.2f}")
c.drawString(100, 690, f"Aggregated Total Amount: {aggregated_total_amount:.2f}")
c.drawString(100, 670, "Recommendations:")

# Add recommendations
c.drawString(120, 650, "- Conduct regular anomaly detection checks.")
c.drawString(120, 630, "- Implement stricter validation rules for high-value transactions.")
c.drawString(120, 610, "- Enhance data quality control measures.")

# Draw the image on the PDF (centered)
c.drawImage(ImageReader(buffer), 100, 250, width=400, height=200)

# Save the PDF
c.save()

# Show plot (optional)
plt.show()
