import os
import csv
import codecs
import logging
from datetime import datetime
import argparse
from typing import List, Tuple, Optional
from pathlib import Path

def detect_encoding(file_path: str) -> Optional[str]:
    """
    Detects the encoding of a given file by attempting to read it with UTF-8 and Shift-JIS.

    Args:
        file_path (str): Path to the file to be checked.

    Returns:
        Optional[str]: Detected encoding if successful, None otherwise.
    """
    encodings = ['utf-8', 'shift-jis']
    for encoding in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    return None

def read_replace_pairs(csv_file: str) -> List[Tuple[str, str]]:
    """
    Reads replacement pairs from a CSV file and logs any additional notes found.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        List[Tuple[str, str]]: List of tuples containing find and replace text.

    Raises:
        ValueError: If the file encoding cannot be detected.
    """
    encoding = detect_encoding(csv_file)
    if encoding is None:
        raise ValueError("Unable to detect file encoding for the CSV file.")
    
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

def find_and_replace_in_file(file_path: str, find_text: str, replace_text: str) -> None:
    """
    Performs find and replace in a file with UTF-8 error handling and logs the result.

    Args:
        file_path (str): Path to the file to be processed.
        find_text (str): Text to find in the file.
        replace_text (str): Text to replace the found text with.
    """
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as file:
            content = file.read()

        new_content = content.replace(find_text, replace_text)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8-sig') as file:
                file.write(new_content)
            logging.info(f"Replaced '{find_text}' with '{replace_text}' in {file_path}")
        else:
            logging.debug(f"No change for '{find_text}' in {file_path}.")

    except PermissionError as e:
        logging.error(f"Permission error while processing {file_path}: {e}.")
    except Exception as e:
        logging.error(f"An error occurred while processing {file_path}: {e}.")

def initialize_logging(log_level: int, destination: str) -> str:
    """
    Initializes the logging configuration and creates a log file with a UTF-8 BOM.

    Args:
        log_level (int): The logging level.
        destination (str): Directory where the log file will be saved.

    Returns:
        str: Path to the log file created.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"replace_log_{timestamp}.txt"
    log_file_path = os.path.join(destination, log_file_name)

    with open(log_file_path, 'w', encoding='utf-8-sig') as log_file:
        log_file.write('\ufeff')

    logging.basicConfig(
        filename=log_file_path,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a',
        encoding='utf-8-sig'
    )
    logging.info("Logging initialized.")
    return log_file_path

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the batch find and replace tool.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Batch find and replace tool for HTML/JS files.")
    parser.add_argument("-s", "--source", required=True, help="Path to the CSV file containing find and replace instructions.")
    parser.add_argument("-t", "--target", required=True, help="Path to the directory where replacements will be performed.")
    parser.add_argument("-l", "--log", choices=["NONE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="NONE", help="Set the logging level (default: NONE).")
    return parser.parse_args()

def main() -> None:
    """
    Main function to run the batch find and replace operation.
    """
    args = parse_arguments()

    csv_file_path = args.source
    target_directory = Path(args.target).resolve() # args.target
    log_level = getattr(logging, args.log) if args.log != "NONE" else logging.CRITICAL

    if args.log != "NONE":
        log_file_path = initialize_logging(log_level, os.path.dirname(csv_file_path))
        print(f"Log file created: {log_file_path}")
    else:
        logging.basicConfig(level=logging.CRITICAL)
        print("Logging is disabled.")

    try:
        find_replace_pairs = read_replace_pairs(csv_file_path)
    except ValueError as e:
        print(f"Error reading CSV file: {e}")
        logging.error(f"Error reading CSV file: {e}")
        return

    for root, _, files in os.walk(target_directory):
        for file_name in files:
            if file_name.lower().endswith(('.html', '.js')):
                file_path = os.path.join(root, file_name)
                for find_text, replace_text in find_replace_pairs:
                    find_and_replace_in_file(file_path, find_text, replace_text)

    logging.info("Replacement operation completed.")
    print("Replacement operation completed.")

if __name__ == "__main__":
    main()