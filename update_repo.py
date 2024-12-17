import os
import subprocess
from datetime import datetime

# GitHub Repo Commit and Push Automation
def git_push():
    try:
        # Pull the latest changes from GitHub(changed from my mac😁)
        # this creates 30 min latency in actually updating website
        # when midifing things from my mac(or any other devide locally)
        # if want to implement fast(remove 30 min latency), one shall update from server
        subprocess.run(["git", "pull", "origin", "main"], check=True)


        # Check if there are changes to commit
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

        # If there are no changes, skip commit and push
        if not status_result.stdout:
            print("No changes to commit. Skipping commit and push.")
            return
        # well why not ?? hehe 😜


        # Add changes to git
        # subprocess.run(["git", "add", "logs.csv", "README.md"], check=True)

        # above add ws to update table, but creates problem while updating logic for server so
        # until the server is totally fixed for 60 days use below add all


        # Add all changes to git (stages all modified files)
        subprocess.run(["git", "add", "."], check=True)
        # Commit the changes with a timestamp message



        commit_message = f"Auto-update logs at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
        subprocess.run(["git", "push"], check=True)

        print("✅ Changes pushed to GitHub successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    git_push()