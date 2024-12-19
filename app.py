from flask import Flask, render_template, request
from datetime import datetime
import csv
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

app = Flask(__name__)

# Get the absolute path of the current script
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))#for local project if needed
BASE_DIR = os.path.join(os.path.expanduser("~"), "aakku106", "first")#for server

# Path to the CSV file
LOG_FILE = os.path.join(BASE_DIR, "logs.csv")

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["S.N", "Logic/Function", "Date and Time"])



def call_update_repo():
    """
    Call the update_repo.py script every 30 minutes.
    """
    try:
        # Run update_repo.py using Python
        script_path = os.path.join(BASE_DIR, "update_repo.py")
        subprocess.run(["python3", script_path], check=True)  # Adjust to "python" if using Python 2
        print("✅ update_repo.py executed successfully!")
    except Exception as e:
        print(f"❌ Error executing update_repo.py: {e}")


# Scheduler to run call_update_repo every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(call_update_repo, 'interval', minutes=30)
scheduler.start()


@app.route('/index', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        logic_name = request.form.get('logic_name')
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, mode="r") as file:
            reader = list(csv.reader(file))
            sn = len(reader)

        with open(LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([sn, logic_name, date_time])

        message = f"Log saved: {logic_name} at {date_time}"

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