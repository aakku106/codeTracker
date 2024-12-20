from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import csv
import os
import subprocess

app = Flask(__name__)
# Set a secret key for session management
app.secret_key = 'your-secret-key-here'  # Change this to a secure random string

# Your passkey
PASSKEY = "your-secret-passkey"  # Change this to your desired passkey

# Path to the CSV file and README.md file (same folder as app.py)
LOG_FILE = "logs.csv"  # Logs file in the same directory as app.py
README_PATH = "README.md"  # README.md file in the same directory as app.py

# Add this with your other constants at the top
PASSWORD = "YourSecretPassword123"  # Change this to whatever password you want to use

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
    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        passkey = request.form.get('passkey')
        if passkey == PASSKEY:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid passkey!')
            return redirect(url_for('auth'))
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
    # Check password before processing
    if request.form.get('password') != PASSWORD:
        return "Incorrect password!", 403
    
    # Get the current count from the CSV file
    try:
        with open(LOG_FILE, mode="r") as file:
            count = sum(1 for line in file) - 1  # Subtract 1 for header row
    except FileNotFoundError:
        count = 0

    # Your existing submit logic
    logic = request.form.get('logic')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create row data as a list
    row_data = [count + 1, logic, current_time]
    
    # Write to CSV
    safe_write_to_csv(row_data)
    
    # Update README
    update_readme()
    
    return redirect(url_for('index'))

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
