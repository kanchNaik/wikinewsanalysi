import subprocess
import os
from wikinews_app.Algos.DecayingWindowAlgo import run_decaying_window_algo
from wikinews_app.Algos.Producer import publish_wiki_pageviews

def task1():
    log_file_path = r'C:\Users\naikn\OneDrive\Desktop\Repos\WikipediaNewsArticlesAnalysis\Backend\wikinews\wikinews_app\logs\producer_logs.log'

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    try:
        # Open log file for appending
        with open(log_file_path, 'a') as log_file:
            # Redirect standard output and error to the log file
            original_stdout = os.sys.stdout
            original_stderr = os.sys.stderr
            os.sys.stdout = log_file
            os.sys.stderr = log_file

            # Call the function directly
            print("Starting Decaying Window Algorithm...")
            publish_wiki_pageviews(r"C:\Users\naikn\Downloads\pageviews-20240131-230000.gz")
            print("Decaying Window Algorithm completed successfully.")

            # Restore standard output and error
            os.sys.stdout = original_stdout
            os.sys.stderr = original_stderr
    except Exception as e:
        # Restore standard output and error in case of errors
        os.sys.stdout = original_stdout
        os.sys.stderr = original_stderr
        print(f"An error occurred while running the decaying window algorithm: {e}")

def task2():
    log_file_path = r'C:\Users\naikn\OneDrive\Desktop\Repos\WikipediaNewsArticlesAnalysis\Backend\wikinews\wikinews_app\logs\decayingwindowlogs.log'

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    try:
        # Open log file for appending
        with open(log_file_path, 'a') as log_file:
            # Redirect standard output and error to the log file
            original_stdout = os.sys.stdout
            original_stderr = os.sys.stderr
            os.sys.stdout = log_file
            os.sys.stderr = log_file

            # Call the function directly
            print("Starting Decaying Window Algorithm...")
            run_decaying_window_algo()
            print("Decaying Window Algorithm completed successfully.")

            # Restore standard output and error
            os.sys.stdout = original_stdout
            os.sys.stderr = original_stderr
    except Exception as e:
        # Restore standard output and error in case of errors
        os.sys.stdout = original_stdout
        os.sys.stderr = original_stderr
        print(f"An error occurred while running the decaying window algorithm: {e}")