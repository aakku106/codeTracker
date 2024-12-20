import subprocess
from datetime import datetime
import logging
import os

# Set up logging to write to a file in your project directory
log_file = os.path.join(os.path.dirname(__file__), 'git_update.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def git_push():
    try:
        # Change to the correct directory
        repo_path = '/home/aakku106/first'
        os.chdir(repo_path)
        logging.info(f"Changed directory to: {repo_path}")

        # Configure Git (important for automated tasks)
        subprocess.run(["git", "config", "--global", "user.email", "your-email@example.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Your Name"], check=True)

        # Pull the latest changes from GitHub
        logging.info("Pulling latest changes from GitHub...")
        subprocess.run(["git", "pull", "origin", "main"], check=True)

        # Check if there are changes to commit
        status_result = subprocess.run(["git", "status", "--porcelain"],
                                     capture_output=True, text=True)

        if not status_result.stdout:
            logging.info("No changes to commit. Skipping commit and push.")
            return

        # Add all changes to git
        logging.info("Staging changes...")
        subprocess.run(["git", "add", "."], check=True)

        # Commit the changes with a timestamp message
        commit_message = f"Auto-update logs at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        logging.info(f"Committing with message: {commit_message}")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
        logging.info("Pushing changes to GitHub...")
        subprocess.run(["git", "push"], check=True)

        logging.info("✅ Changes pushed to GitHub successfully!")

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Git operation failed: {e}")
        logging.error(f"Command: {e.cmd}")
        logging.error(f"Output: {e.output if hasattr(e, 'output') else 'No output'}")
        raise
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    git_push()