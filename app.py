from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import threading
from threading import Lock

app = Flask(__name__)

# Path to the CSV file and README.md file (same folder as app.py)
LOG_FILE = "logs.csv"  # Logs file in the same directory as app.py
README_PATH = "README.md"  # README.md file in the same directory as app.py

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["S.N", "Logic/Function", "Date and Time"])

# Lock to prevent multiple overlapping executions of the update_repo.py script
update_lock = Lock()

def call_update_repo():
    """
    Call the update_repo.py script every 30 minutes.
    Includes locking to prevent overlapping executions.
    """
    if update_lock.locked():
        print("🔒 Previous job still running. Skipping this interval.")
        return

    with update_lock:
        try:
            script_path = os.path.join("update_repo.py")
            subprocess.run(["python", script_path], check=True)
            print("✅ update_repo.py executed successfully!")
        except Exception as e:
            error_log = f"❌ Error executing update_repo.py: {e}"
            print(error_log)
            with open(LOG_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Error", "Update Repo Script", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

# Scheduler to run call_update_repo every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(call_update_repo, 'interval', minutes=30)
def start_scheduler():
    if not scheduler.running:
        scheduler.start()

# Only start the scheduler if running in a non-uWSGI context
if 'uwsgi' not in globals():
    start_scheduler()
# scheduler.start()

def update_readme():
    """
    Update the README.md file with the logs from logs.csv.
    This will format the logs into a Markdown table.
    """
    # Read logs from logs.csv
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        logs = reader[1:]  # Skip the header row

    # Prepare the Markdown table
    table_header = "| S.N | Logic/Function | Date and Time |"
    table_divider = "|-----|----------------|---------------|"
    table_rows = []
    for log in logs:
        if len(log) == 3:
            sn, logic, date_time = log
            table_rows.append(f"| {sn} | {logic} | {date_time} |")
        else:
            print(f"Skipping incomplete log entry: {log}")

    # Combine the table parts
    markdown_table = "\n".join([table_header, table_divider] + table_rows)

    # Write the table to the README.md file
    try:
        with open(README_PATH, mode="a") as readme_file:
            readme_file.write("\n\n## Log Table\n")  # Add a section for the log table
            readme_file.write(markdown_table)  # Append the table
            print("✅ README.md updated successfully!")
    except Exception as e:
        print(f"❌ Error updating README.md: {e}")
        with open(LOG_FILE, mode="a", newline="") as log_file:
            writer = csv.writer(log_file)
            writer.writerow(["Error", "Update README.md", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def safe_write_to_csv(row_data):
    """Safely write a row to the CSV file with error handling"""
    try:
        with open(LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row_data)
        return True
    except IOError as e:
        print(f"Error writing to CSV: {e}")
        return False

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        try:
            logic_name = request.form.get('logic_name')
            if not logic_name:
                message = "Error: Logic name cannot be empty"
                return render_template('index.html', message=message)

            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(LOG_FILE, mode="r") as file:
                reader = list(csv.reader(file))
                sn = len(reader)

            if safe_write_to_csv([sn, logic_name, date_time]):
                update_readme()
                message = f"Log saved: {logic_name} at {date_time}"
            else:
                message = "Error: Failed to save log"
        except Exception as e:
            message = f"Error: {str(e)}"

    return render_template('index.html', message=message)

@app.route('/logs')
def view_logs():
    with open(LOG_FILE, mode="r") as file:
        reader = list(csv.reader(file))
        reversed_logs = reader[1:][::-1]
    return render_template('logs.html', logs=reversed_logs)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
