## 📖 Table of Contents

- [📖 Table of Contents](#-table-of-contents)
- [📝Description](#description)
- [✨Features](#features)
- [⚙️Installation Instructions](#️installation-instructions)
- [🚀 Usage Guide](#-usage-guide)
    - [Command-line Options and Parameters](#command-line-options-and-parameters)
    - [CSV File Format](#csv-file-format)
        - [Column Definitions](#column-definitions)
        - [CSV Format Requirements](#csv-format-requirements)
        - [Sample CSV File](#sample-csv-file)
            - [**Explanation**](#explanation)
- [📁 Examples](#-examples)
- [🔬 How It Works](#-how-it-works)
- [✅ Prerequisites](#-prerequisites)
- [📜 License](#-license)
- [📬 Contact Information](#-contact-information)

## 📝Description

A command-line tool designed to perform batch find and replace operations across HTML and JS files within a specified directory, using a CSV file for replacement instructions. The tool supports UTF-8 and Shift-JIS encoded files and logs operations for transparency.

## ✨Features

- Reads find-and-replace pairs from a CSV file.
- Detects file encoding (UTF-8 and Shift-JIS).
- Processes files with UTF-8 error handling.
- Logs operations to a UTF-8 BOM log file.
- Command-line interface with easy-to-use options.

## ⚙️Installation Instructions

1. Ensure Python 3.9 or higher is installed.
2. Clone this repository or download the script.
3. Install any necessary dependencies (e.g., `pip install -r requirements.txt`).

## 🚀 Usage Guide

Run the script from the command line with the following syntax:

```sh
python batrepl.py -s <path_to_csv> -t <target_directory> -l <log_level>
```

### Command-line Options and Parameters

- `-s, --source`: Path to the CSV file containing find-and-replace instructions (required).
- `-t, --target`: Path to the directory where the replacements will be performed (required).
- `-l, --log`: Logging level (`NONE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default is `NONE`.

### CSV File Format

The input CSV file should contain rows where each row specifies a "find" text and its corresponding "replace" text. An optional third column can include notes, which are logged during processing but do not affect the replacement process.

#### Column Definitions

1. **Find Text (Column 1)**: The text to search for in the target files.
2. **Replace Text (Column 2)**: The text that will replace occurrences of the "find" text.
3. **Notes (Optional, Column 3)**: Additional notes related to the replacement. These are logged for informational purposes.

#### CSV Format Requirements

- The file encoding must be either UTF-8 or Shift-JIS. The program will attempt to detect and read the correct encoding.
- Double quotes (`""`) within cells should be interpreted as a single quote (`"`).

#### Sample CSV File

```csv
find_text_simple,replace_text_simple,Example without double quotes
"find_text_1","replace_text_1","This is a note about the first replacement"
"find_text_2","replace_text_2"
"special_characters_&_symbols","updated_version","Handles & symbols"
"text_with_quotes","text with ""escaped quotes""","Double quotes in the text"
```

##### **Explanation**

- The first row shows a simple find-and-replace without surrounding double quotes.
- The second row replaces `find_text_1` with `replace_text_1` and logs a note.
- The third row performs a simple replacement without logging a note.
- The fourth row demonstrates handling special characters and symbols.
- The fifth row shows how to escape double quotes within text using double double quotes.

## 📁 Examples

1. **Basic Replacement with Logging Enabled**:

   ```sh
   python batrepl.py -s replacements.csv -t ./website_files -l INFO
   ```

   This command reads replacement pairs from `replacements.csv`, performs replacements in all `.html` and `.js` files within the `website_files` directory, and logs actions at the `INFO` level.

2. **Replacement with Logging Disabled (Implicit)**:

   ```sh
   python batrepl.py -s replacements.csv -t ./project_folder
   ```

   This command runs the tool without generating any logs, as logging is disabled by default.

3. **Replacement with Logging Disabled (Explicit)**:

   ```sh
   python batrepl.py -s replacements.csv -t ./project_folder -l NONE
   ```

   This command also runs the tool without logging, but here the `-l NONE` parameter explicitly disables logging.

4. **Processing a Large Directory with Debug Logs**:

   ```sh
   python batrepl.py -s find_replace_pairs.csv -t /var/www/html -l DEBUG
   ```

   This command reads replacement instructions from `find_replace_pairs.csv`, processes all matching files in the `/var/www/html` directory, and logs detailed debug information.

5. **Replacing Content in a Specific Subdirectory**:

   ```sh
   python batrepl.py -s replace_list.csv -t ./app/scripts -l WARNING
   ```

   This command applies replacements only within the `./app/scripts` directory and logs warnings or higher-level messages.

6. **Verbose Logging for Testing Purposes**:

   ```sh
   python batrepl.py -s test_pairs.csv -t ./sandbox -l DEBUG
   ```

   Ideal for testing and development, this command runs with `DEBUG` logging to provide in-depth details about each replacement action in the `./sandbox` directory.

## 🔬 How It Works

1. The tool detects the encoding of the provided CSV file and reads find-and-replace pairs.
2. It recursively scans the target directory for `.html` and `.js` files.
3. Each file is read and modified if a match is found, and the result is saved.
4. Logs are created in a specified location if logging is enabled.

## ✅ Prerequisites

- Python 3.9 or higher
- `argparse`, `csv`, `codecs`, `logging`, and `pathlib` modules (standard Python library).

## 📜 License

This project is licensed under the MIT License. You can use, copy, modify, and distribute this software under the terms of the MIT License. See the [LICENSE](LICENSE.md) file for the full text.

## 📬 Contact Information

For any questions or support, please contact the [authors](authors.md).
