from flask import Flask, request, jsonify
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


@app.route('/')
def home():
    return "Hello, Aakku! Flask is running 🎉"


@app.route('/log', methods=['POST', 'GET'])
def log_work():
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

        return f"Log saved: {logic_name} at {date_time}"

    # Display the form for input
    return '''
        <form method="POST">
            Logic/Function Worked On: <input type="text" name="logic_name">
            <input type="submit" value="Log Work">
        </form>
        <br>
        <a href="/logs">View Logs</a>
    '''


@app.route('/logs')
def view_logs():
    # Read and display the logs from the CSV file
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        log_html = "<h2>Work Logs</h2><ul>"
        for row in reader[1:]:  # Skip the header
            log_html += f"<li>S.N: {row[0]} | {row[1]} | {row[2]}</li>"
        log_html += "</ul>"
    return log_html



# Update README.md with the latest logs
def update_readme():
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        with open("README.md", "w") as readme:
            readme.write("# Work Logs 🚀\n\n")
            readme.write("| S.N | Logic/Function | Date and Time |\n")
            readme.write("| --- | -------------- | ------------- |\n")
            for row in reader[1:]:
                readme.write(f"| {row[0]} | {row[1]} | {row[2]} |\n")

# Call update_readme after writing to CSV
update_readme()

import subprocess

# After updating the CSV and README
subprocess.run(["python", "update_repo.py"])

if __name__ == '__main__':
    app.run(debug=True)