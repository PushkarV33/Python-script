import csv
from datetime import datetime
from fpdf import FPDF

# Current date from the system (hardcoded for this example; in a real script, use datetime.now())
CURRENT_DATE = "Wednesday, July 23, 2025, 4:03 PM IST"

# Function to read and analyze data from CSV


def read_and_analyze_data(file_path):
    data = []
    total_quantity = 0
    total_revenue = 0.0
    prices = []
    top_product = None
    max_quantity = 0

    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                quantity = int(row['Quantity'])
                price = float(row['Price'])
                revenue = quantity * price

                data.append({
                    'Product': row['Product'],
                    'Quantity': quantity,
                    'Price': price,
                    'Revenue': revenue
                })

                total_quantity += quantity
                total_revenue += revenue
                prices.append(price)

                if quantity > max_quantity:
                    max_quantity = quantity
                    top_product = row['Product']

        if not data:
            raise ValueError("No data found in the file.")

        num_items = len(data)
        average_price = sum(prices) / num_items if num_items > 0 else 0

        analysis = {
            'total_quantity': total_quantity,
            'total_revenue': total_revenue,
            'average_price': average_price,
            'top_product': top_product,
            'num_items': num_items
        }

        return data, analysis

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading/analyzing data: {str(e)}")

# Function to generate PDF report


def generate_pdf_report(data, analysis, output_path='report.pdf'):
    pdf = FPDF()
    pdf.add_page()

    # Set font for title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Sales Data Analysis Report", ln=True, align='C')

    # Add date
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, txt=f"Generated on: {CURRENT_DATE}", ln=True, align='C')
    pdf.ln(10)  # Line break

    # Summary section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Summary Statistics", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Total Items: {analysis['num_items']}", ln=True)
    pdf.cell(
        200, 10, txt=f"Total Quantity Sold: {analysis['total_quantity']}", ln=True)
    pdf.cell(
        200, 10, txt=f"Total Revenue: ${analysis['total_revenue']:.2f}", ln=True)
    pdf.cell(
        200, 10, txt=f"Average Price: ${analysis['average_price']:.2f}", ln=True)
    pdf.cell(
        200, 10, txt=f"Top Selling Product: {analysis['top_product']} (Quantity: {analysis['total_quantity']})", ln=True)
    pdf.ln(10)

    # Data table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Detailed Data", ln=True)

    # Table headers
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "Product", border=1)
    pdf.cell(40, 10, "Quantity", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(40, 10, "Revenue", border=1)
    pdf.ln()

    # Table rows
    pdf.set_font("Arial", '', 10)
    for item in data:
        pdf.cell(50, 10, item['Product'], border=1)
        pdf.cell(40, 10, str(item['Quantity']), border=1)
        pdf.cell(40, 10, f"${item['Price']:.2f}", border=1)
        pdf.cell(40, 10, f"${item['Revenue']:.2f}", border=1)
        pdf.ln()

    # Output the PDF
    pdf.output(output_path)
    print(f"PDF report generated: {output_path}")


# Main execution
if __name__ == "__main__":
    file_path = 'data.csv'  # Change this to your file path
    try:
        data, analysis = read_and_analyze_data(file_path)
        generate_pdf_report(data, analysis)
    except Exception as e:
        print(f"Error: {str(e)}")
