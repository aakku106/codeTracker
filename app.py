from flask import Flask, render_template, request
from datetime import datetime
import csv
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

app = Flask(__name__)

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the CSV file
LOG_FILE = os.path.join(BASE_DIR, "logs.csv")

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["S.N", "Logic/Function", "Date and Time"])


def auto_push():
    """
    Automatically push updates every 30 minutes.
    """
    try:
        # Run git commands
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Auto-push executed successfully!")
    except Exception as e:
        print(f"Error during auto-push: {e}")


# Scheduler to run auto_push every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(auto_push, 'interval', minutes=30)
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