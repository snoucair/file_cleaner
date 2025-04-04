import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog
import string

# Function to process a single file
def process_file(input_filepath, output_filepath):
    try:
        # Read the file with 'replace' error strategy to handle unusual encodings
        with open(input_filepath, 'r', encoding='utf-8', errors='replace') as infile:
            lines = infile.readlines()

        # Define allowed characters (whitelist approach)
        allowed_chars = set(string.ascii_letters + string.digits + '+-_:;,.=/\\*() \t\n\r')

        clean_lines = []
        removed_count = 0

        for line in lines:
            # Check if line starts with P1 or P2 - always keep these
            if line.strip().startswith('P1') or line.strip().startswith('P2'):
                clean_lines.append(line)
                continue

            # Check if all characters in the line are in the allowed set
            has_invalid_char = any(char not in allowed_chars for char in line)

            if has_invalid_char:
                # Skip the detailed display of removed lines
                removed_count += 1
            else:
                clean_lines.append(line)

        # Write cleaned lines to output file
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.writelines(clean_lines)

        st.write(f"  - Removed {removed_count} lines with invalid characters")
        return True, None
    except Exception as e:
        return False, str(e)

# --- Streamlit App UI ---

st.title("File Cleaner - Whitelist Approach")

st.write("This app processes all files in the input folder, removes lines with non-standard characters, and saves the cleaned files to the output folder.")

# Initialize session state for folder paths
if 'input_folder' not in st.session_state:
    st.session_state['input_folder'] = None
if 'output_folder' not in st.session_state:
    st.session_state['output_folder'] = None

# --- Folder Selection ---
# Tkinter setup for folder dialog
root = tk.Tk()
root.withdraw() # Hide the main tkinter window
root.wm_attributes('-topmost', 1) # Keep dialog on top

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Folder")
    if st.button("Select Input Folder"):
        input_folder = filedialog.askdirectory(master=root, title="Choose Input Folder")
        if input_folder:
            st.session_state['input_folder'] = input_folder
    if st.session_state['input_folder']:
        st.write(f"Selected: `{st.session_state['input_folder']}`")
    else:
        st.write("No folder selected.")

with col2:
    st.subheader("Output Folder")
    if st.button("Select Output Folder"):
        output_folder = filedialog.askdirectory(master=root, title="Choose Output Folder")
        if output_folder:
            st.session_state['output_folder'] = output_folder
    if st.session_state['output_folder']:
        st.write(f"Selected: `{st.session_state['output_folder']}`")
    else:
        st.write("No folder selected.")

st.divider()

# --- Processing ---
if st.button("Process Files", disabled=(not st.session_state['input_folder'] or not st.session_state['output_folder'])):
    input_dir = st.session_state['input_folder']
    output_dir = st.session_state['output_folder']

    if not os.path.isdir(input_dir):
        st.error("Input folder does not exist.")
    elif not os.path.isdir(output_dir):
        st.error("Output folder does not exist. Please create it or select a valid one.")
    else:
        st.info(f"Starting processing...")
        processed_count = 0
        error_count = 0
        files_processed = []
        files_with_errors = []

        try:
            for filename in os.listdir(input_dir):
                # Process all files in the input folder
                if os.path.isfile(os.path.join(input_dir, filename)):
                    input_filepath = os.path.join(input_dir, filename)
                    output_filepath = os.path.join(output_dir, filename) # Keep original filename

                    st.write(f"Processing: {filename}")
                    success, error_msg = process_file(input_filepath, output_filepath)

                    if success:
                        processed_count += 1
                        files_processed.append(filename)
                        st.write(f"  - Successfully cleaned and saved to: {output_filepath}")
                    else:
                        error_count += 1
                        files_with_errors.append(f"{filename} ({error_msg})")
                        st.error(f"  - Error processing {filename}: {error_msg}")

            st.success(f"Processing complete!")
            st.write(f"Total files processed: {processed_count}")
            st.write(f"Files successfully cleaned: {', '.join(files_processed) if files_processed else 'None'}")
            if error_count > 0:
                st.warning(f"Files with errors: {error_count}")
                st.write(f"Errors occurred in: {', '.join(files_with_errors)}")

        except Exception as e:
            st.error(f"An unexpected error occurred during processing: {str(e)}")

# Instructions to run
st.sidebar.header("How to Run")
st.sidebar.markdown("""
1. Save this code as a Python file (e.g., `file_cleaner.py`).
2. Make sure you have Python, Streamlit, and Tkinter installed:
   ```bash
   pip install streamlit
   # Tkinter is usually included with Python standard library
   ```
3. Run the app from your terminal:
   ```bash
   streamlit run file_cleaner.py
   ```
4. Use the buttons in the web interface to select folders and process files.
""")
# Created/Modified files during execution:
# Note: This script processes all files in the input directory and creates cleaned versions in the output directory.
print("Created/Modified files during execution:")
print("All files in the selected input folder will be processed and saved to the output folder.")