from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
import os
import subprocess

app = Flask(__name__)

# Path to the CSV file and README.md file (same folder as app.py)
LOG_FILE = "logs.csv"  # Logs file in the same directory as app.py
README_PATH = "README.md"  # README.md file in the same directory as app.py

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["S.N", "Logic/Function", "Date and Time"])

def call_update_repo():
    """
    Call the update_repo.py script.
    """
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

def update_readme():
    """Update the README.md file with the current logs."""
    try:
        # Read the CSV file
        with open(LOG_FILE, mode="r") as file:
            csv_reader = csv.reader(file)
            # Skip the header row
            next(csv_reader)
            # Convert to list and sort by S.N
            logs = sorted(list(csv_reader), key=lambda x: int(x[0]) if x[0].isdigit() else 0)

        # Create the README content
        readme_content = """# Work Logs 🚀

| S.N | Logic/Function | Date and Time |
|-----|---------------|---------------|
"""
        # Add each log entry
        for log in logs:
            readme_content += f"| {log[0]} | {log[1]} | {log[2]} |\n"

        # Write to README.md (overwrite the entire file)
        with open(README_PATH, mode="w", encoding="utf-8") as file:
            file.write(readme_content)

    except Exception as e:
        print(f"Error updating README: {e}")

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
