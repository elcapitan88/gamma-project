from flask import Flask, send_file
import requests
from bs4 import BeautifulSoup
import io

app = Flask(__name__)

@app.route('/download_csv')
def download_csv():
    # Step 1: Fetch the web page
    response = requests.get("https://www.cboe.com/delayed_quotes/spy/quote_table")
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Step 2: Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Find the URL of the CSV file (this part may need to be customized)
    csv_url = None
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and 'csv' in href:
            csv_url = href
            break

    # Step 4: Download the CSV file
    if csv_url:
        csv_response = requests.get(csv_url)
        csv_response.raise_for_status()
        csv_data = csv_response.content
        return send_file(io.BytesIO(csv_data),
                         attachment_filename='data.csv',
                         as_attachment=True,
                         mimetype='text/csv')
    else:
        return "CSV file not found."

if __name__ == '__main__':
    app.run(debug=True)
