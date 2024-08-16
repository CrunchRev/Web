import subprocess
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()

def check_for_updates():
    fetch_stdout, fetch_stderr = run_command('git fetch')

    if "fatal:" in fetch_stderr or "error:" in fetch_stderr:
        logging.error(f"Error fetching updates: {fetch_stderr}")
        return False
    
    log_stdout, log_stderr = run_command('git log HEAD..origin/main --oneline')
    if log_stdout:
        logging.info("Updates are available.")
        return True
    elif log_stderr:
        logging.error(f"Error checking for updates: {log_stderr}")
        return False
    else:
        logging.info("No updates available.")
        return False

def stash_and_pull_updates():
    logging.info("Stashing local changes...")
    stash_stdout, stash_stderr = run_command('git stash')
    if "fatal:" in stash_stderr or "error:" in stash_stderr:
        logging.error(f"Error stashing changes: {stash_stderr}")
        return False
    
    logging.info("Pulling latest changes...")
    pull_stdout, pull_stderr = run_command('git pull')
    if "fatal:" in pull_stderr or "error:" in pull_stderr:
        logging.error(f"Error pulling updates: {pull_stderr}")
        return False

    return True

def terminate_python_process():
    logging.info("Terminating Python process...")
    if os.name == 'nt':
        run_command('taskkill /f /im python.exe')
    else:
        run_command('pkill -f python')

def main():
    os.chdir(r'C:\Web')
    while True:
        if check_for_updates():
            if stash_and_pull_updates():
                terminate_python_process()
            else:
                logging.error("Failed to update. Please check the error messages above.")
        else:
            logging.info("No updates needed.")
        
        logging.info("Checking for updates again in 15 seconds...")
        time.sleep(15)

if __name__ == "__main__":
    main()
