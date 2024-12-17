import os
import subprocess
from datetime import datetime

# GitHub Repo Commit and Push Automation
def git_push():
    try:
        # Fetch the GitHub token from environment variables
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GitHub token not found in environment variables!")

        # Set the remote URL with the token for authentication
        repo_url = f"https://{github_token}:x-oauth-basic@github.com/aakku106/codeTracker.git"

        # Add changes to git
        subprocess.run(["git", "add", "logs.csv", "README.md"], check=True)

        # Commit the changes with a timestamp message
        commit_message = f"Auto-update logs at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes using the token in the remote URL
        subprocess.run(["git", "push", repo_url], check=True)

        print("✅ Changes pushed to GitHub successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error:", e)
    except ValueError as ve:
        print("❌ Error:", ve)

if __name__ == "__main__":
    git_push()