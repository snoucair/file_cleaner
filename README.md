# Text Cleaner

A Streamlit-based application for cleaning text files by removing lines containing non-standard characters while preserving specific patterns.

## Features

- User-friendly web interface built with Streamlit
- Processes multiple files in batch
- Removes lines containing non-standard characters
- Supports UTF-8 encoding with fallback error handling
- Shows detailed processing statistics and results

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
```bash
pip install streamlit
```
Note: Tkinter is typically included with Python's standard library.

## Usage

1. Run the application:
```bash
streamlit run valo_text_cleaner_app.py
```

2. In the web interface:
   - Click "Select Input Folder" to choose the folder containing files to process
   - Click "Select Output Folder" to specify where cleaned files should be saved
   - Click "Process Files" to start the cleaning operation

## Allowed Characters

The application uses a whitelist approach and allows only the following characters:
- ASCII letters (a-z, A-Z)
- Numbers (0-9)
- Special characters: +-_:;,.=/\*()
- Whitespace characters (space, tab, newline)

## Output

- Cleaned files are saved to the output folder with the same filename as the input
- The application provides statistics on:
  - Number of files processed
  - Number of lines removed
  - Any errors encountered during processing
