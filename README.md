# Text Cleaner

A Streamlit-based application for cleaning text files by removing lines containing non-standard characters while preserving specific patterns, and splitting files based on markers.

## Features

- User-friendly web interface built with Streamlit
- **Clean Files**: Removes lines containing non-standard characters
- **Split Files**: Splits large files into smaller files based on P1 markers
- Processes multiple files in batch
- Real-time progress tracking with progress bars
- Preserves lines starting with P1 or P2 markers regardless of content
- Supports UTF-8 encoding with fallback error handling
- Shows detailed processing statistics and results

## Installation

### Prerequisites

- Python 3.7+ installed on your system
- Basic familiarity with running commands in a terminal/command prompt

### Step-by-Step Installation for Beginners

1. **Install Python** (if not already installed):
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening a command prompt/terminal and typing:
     ```
     python --version
     ```

2. **Clone or download this repository**:
   - If you have Git:
     ```bash
     git clone https://github.com/snoucair/file_cleaner.git
     cd file_cleaner
     ```
   - If you don't have Git:
     - Download the ZIP file from GitHub
     - Extract it to a folder on your computer
     - Open a command prompt/terminal and navigate to the extracted folder:
       ```bash
       cd path/to/extracted/folder
       ```

3. **Create a virtual environment** (recommended but optional):
   - Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide for Beginners

1. **Start the application**:
   ```bash
   streamlit run text_cleaner_app.py
   ```
   - This will open the application in your default web browser
   - If it doesn't open automatically, look for a URL in the terminal (usually http://localhost:8501)

2. **Using the application**:

   a. **Select Input and Output Folders**:
   - Click "Select Input Folder" to choose the folder containing files to process
   - Click "Select Output Folder" to specify where processed files should be saved
   
   b. **Choose Processing Option**:
   - **Clean Files**: Removes lines with non-standard characters
   - **Split Files**: Splits files based on P1 markers into multiple smaller files
   
   c. **Process Files**:
   - Click "Process Files" or "Split Files" button depending on your selected option
   - Wait for processing to complete
   - Review the results and statistics displayed

3. **Interpreting Results**:
   - The app shows a summary of processed files
   - For successful operations, you'll see counts of files processed
   - For any errors, the app will display which files had issues

## Understanding the Cleaning Process

- **Character Whitelist**: The application only allows these characters:
  - ASCII letters (a-z, A-Z)
  - Numbers (0-9)
  - Special characters: +-_:;,.=/\*()
  - Whitespace characters (space, tab, newline)
- **Line Preservation**: Lines starting with P1 or P2 are always preserved regardless of content
- **Output**: Each cleaned file retains its original filename but is saved to the output folder

## Understanding the Splitting Process

- **Split Markers**: Files are split at each occurrence of "P1" in the text
- **File Naming**: Split files are named with the original filename plus a sequence number
  - Example: `original.txt` becomes `original_1.txt`, `original_2.txt`, etc.
- **Progress Tracking**: The app shows real-time progress with a progress bar and running summary

## Troubleshooting

- **Missing libraries**: If you see errors about missing modules, run:
  ```bash
  pip install streamlit tk
  ```

- **Folder selection issues**: Make sure you have permission to access the folders you're selecting

- **File encoding errors**: The app attempts to handle encoding issues automatically, but some files might still cause errors if they use very unusual encodings

## Advanced Tips

- For processing large batches of files, ensure your output folder has sufficient disk space
- The application preserves specific line patterns (P1, P2) which can be useful for maintaining document structure
- You can view the code to understand how the processing works and customize it for your specific needs

## Deployment

The application can be deployed on Streamlit Community Cloud:

1. Fork this repository to your GitHub account
2. Visit [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Click "New app" and select this repository
4. Choose the main branch and the file `text_cleaner_app.py`
5. Click "Deploy"

The app will be available at `https://your-app-name.streamlit.app`