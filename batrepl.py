import os
import csv
import codecs
import logging
from datetime import datetime
import argparse

# Function to detect encoding (UTF-8 or Shift-JIS)
def detect_encoding(file_path):
    encodings = ['utf-8', 'shift-jis']
    for encoding in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    return None

# Function to read the CSV and get the replace pairs
def read_replace_pairs(csv_file):
    encoding = detect_encoding(csv_file)
    if encoding is None:
        raise ValueError("Unable to detect file encoding.")
    
    replace_pairs = []
    with codecs.open(csv_file, 'r', encoding=encoding) as f:
        reader = csv.reader(f, skipinitialspace=True, quotechar='"', doublequote=True)
        for row in reader:
            if len(row) >= 2:
                before_replace = row[0].replace('""', '"')
                after_replace = row[1].replace('""', '"')
                replace_pairs.append((before_replace, after_replace))

                if len(row) > 2:
                    third_column = row[2]
                    logging.info(f"Note: {third_column}")

    return replace_pairs

# Function to perform find and replace in a file with UTF-8 error handling
def find_and_replace_in_file(file_path, find_text, replace_text):
    try:
        # Open the file with UTF-8, replacing invalid characters
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()

        # Perform the replacement
        new_content = content.replace(find_text, replace_text)

        # Only write back if the content has changed
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

            # Log the replacement only if it actually happened
            logging.info(f"Replaced '{find_text}' with '{replace_text}' in {file_path}")
        else:
            logging.debug(f"No replacement for '{find_text}' in {file_path}, content unchanged.")

    except PermissionError as e:
        logging.error(f"Permission error: {e}. Skipping {file_path}.")
    except Exception as e:
        logging.error(f"An error occurred with {file_path}: {e}")

# Function to initialize logging with UTF-8 BOM
def initialize_logging(csv_file_path, log_level):
    # Get the directory where the CSV is located
    csv_directory = os.path.dirname(csv_file_path)

    # Create a log file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"replace_log_{timestamp}.txt"
    log_file_path = os.path.join(csv_directory, log_file_name)

    # Write BOM to the log file manually and use it for logging
    with open(log_file_path, 'w', encoding='utf-8-sig') as log_file:
        log_file.write('\ufeff')  # UTF-8 BOM

    # Set up the logging configuration to use the opened log file
    logging.basicConfig(
        filename=log_file_path,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # Append mode after BOM
    )
    logging.info("Logging started.")
    return log_file_path

# Function to parse command-line arguments (CLI)
def parse_arguments():
    parser = argparse.ArgumentParser(description="batrepl - Batch Find and Replace in HTML/JS Files")
    parser.add_argument(
        "csv_file", 
        help="Path to the CSV file containing the replacement instructions"
    )
    parser.add_argument(
        "target_directory", 
        help="Path to the target directory where replacements will be made"
    )
    parser.add_argument(
        "--log", 
        default="NONE",  # Default to no logging
        choices=["NONE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: NONE, which means no logging)"
    )
    return parser.parse_args()

# Main function
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    csv_file_path = args.csv_file
    target_directory = args.target_directory

    # Check if logging is needed (i.e., --log is not "NONE")
    if args.log_level != "NONE":
        log_level = getattr(logging, args.log_level)
        log_file_path = initialize_logging(csv_file_path, log_level)
        print(f"Log file created: {log_file_path}")
    else:
        logging.basicConfig(level=logging.CRITICAL)  # Disable all logging to file or console
        print("Logging is disabled. No log file will be created.")

    # Read the replacement pairs from the CSV file
    try:
        find_replace_pairs = read_replace_pairs(csv_file_path)
    except ValueError as e:
        logging.error(f"Error reading CSV: {e}")
        exit()

    # Iterate over all files in the target directory and subdirectories
    for root, dirs, files in os.walk(target_directory):
        for file_name in files:
            # Only process .html and .js files
            if file_name.lower().endswith(('.html', '.js')):
                file_path = os.path.join(root, file_name)

                # Perform find-and-replace for each pair in each .html or .js file
                for find_text, replace_text in find_replace_pairs:
                    find_and_replace_in_file(file_path, find_text, replace_text)

    logging.info("Replacement operation completed.")
    print("Replacement operation completed.")
