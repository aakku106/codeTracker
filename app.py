from flask import Flask, render_template, request
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Path to the CSV file
LOG_FILE = "logs.csv"

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["S.N", "Logic/Function", "Date and Time"])

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        # Get the input from the form
        logic_name = request.form.get('logic_name')
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the current log count to determine serial number
        with open(LOG_FILE, mode="r") as file:
            reader = list(csv.reader(file))
            sn = len(reader)  # The count of rows gives the next S.N

        # Append the new log to the CSV file
        with open(LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([sn, logic_name, date_time])

        # After saving, update message
        message = f"Log saved: {logic_name} at {date_time}"

    return render_template('index.html', message=message)

@app.route('/logs')
def logs():
    # Read and display the logs from the CSV file
    logs = []
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        for row in reader[1:]:  # Skip the header
            logs.append(row)

    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)