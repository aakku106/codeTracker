import os
import subprocess
from datetime import datetime

# GitHub Repo Commit and Push Automation
def git_push():
    try:
        # Add all changes to git (stages all modified files)
        subprocess.run(["git", "add", "."], check=True)

        # Commit the changes with a timestamp message
        commit_message = f"Auto-update logs at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes (Git will use cached credentials here)
        subprocess.run(["git", "push"], check=True)

        print("✅ Changes pushed to GitHub successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    git_push()