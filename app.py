from flask import Flask, render_template, request, redirect, url_for
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
    return render_template('index.html')

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

        # After logging, update the README
        update_readme()

        return redirect(url_for('logs'))

    return render_template('log_form.html')

@app.route('/logs')
def logs():
    # Read and display the logs from the CSV file
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        logs = []
        for row in reader[1:]:  # Skip the header
            logs.append({"sn": row[0], "logic": row[1], "date_time": row[2]})

    return render_template('logs.html', logs=logs)

def update_readme():
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        with open("README.md", "w") as readme:
            readme.write("# Work Logs 🚀\n\n")
            readme.write("| S.N | Logic/Function | Date and Time |\n")
            readme.write("| --- | -------------- | ------------- |\n")
            for row in reader[1:]:
                readme.write(f"| {row[0]} | {row[1]} | {row[2]} |\n")

if __name__ == '__main__':
    app.run(debug=True)