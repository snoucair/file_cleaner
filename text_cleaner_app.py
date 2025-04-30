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

# Function to split file based on P1 markers
def split_file(input_filepath, output_folder):
    try:
        # Extract the base filename without extension
        base_filename = os.path.basename(input_filepath)
        filename_without_ext, ext = os.path.splitext(base_filename)
        
        # Read all lines from input file
        with open(input_filepath, 'r', encoding='utf-8', errors='ignore') as infile:
            content = infile.read()
        
        # Split the content by P1 markers
        parts = content.split("P1")
        
        # Remove the first empty part if exists
        if parts and not parts[0].strip():
            parts.pop(0)
            
        # Add the P1 marker back to each part and save as separate files
        files_created = []
        for i, part in enumerate(parts, start=1):
            # Create output filename with sequence number
            output_filename = f"{filename_without_ext}_{i}{ext}"
            output_filepath = os.path.join(output_folder, output_filename)
            
            # Add P1 back to the beginning of each part
            part_content = "P1" + part
            
            # Write the part to a new file
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                outfile.write(part_content)
                
            files_created.append(output_filename)
            
        return True, files_created, len(files_created)
    except Exception as e:
        return False, [], str(e)

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

# --- Processing Options ---
process_option = st.radio(
    "Select Processing Option",
    ["Clean Files", "Split Files"],
    index=0
)

# --- Processing ---
if process_option == "Clean Files":
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

else:  # Split Files
    if st.button("Split Files", disabled=(not st.session_state['input_folder'] or not st.session_state['output_folder'])):
        input_dir = st.session_state['input_folder']
        output_dir = st.session_state['output_folder']

        if not os.path.isdir(input_dir):
            st.error("Input folder does not exist.")
        elif not os.path.isdir(output_dir):
            st.error("Output folder does not exist. Please create it or select a valid one.")
        else:
            st.info(f"Starting file splitting based on P1 markers...")
            progress_container = st.empty()
            progress_text = st.empty()
            
            processed_count = 0
            error_count = 0
            files_processed = []
            files_with_errors = []
            total_split_files = 0
            
            # Files to process - process all files in the input directory
            files_to_process = [f for f in os.listdir(input_dir) 
                              if os.path.isfile(os.path.join(input_dir, f))]
            total_files = len(files_to_process)
            
            progress_bar = st.progress(0)

            try:
                for i, filename in enumerate(files_to_process):
                    input_filepath = os.path.join(input_dir, filename)
                    
                    # Update progress
                    progress_pct = (i / total_files) if total_files > 0 else 0
                    progress_bar.progress(progress_pct)
                    progress_text.text(f"Processing file {i+1} of {total_files}: {filename}")
                    
                    # Process the file
                    success, split_files, split_count = split_file(input_filepath, output_dir)

                    if success:
                        processed_count += 1
                        files_processed.append(filename)
                        total_split_files += split_count
                        
                        # Update running summary in the progress container
                        summary_text = f"""
                        **Running Summary:**
                        - Files processed: {processed_count}/{total_files}
                        - Total split files created: {total_split_files}
                        - Files with errors: {error_count}
                        """
                        progress_container.markdown(summary_text)
                    else:
                        error_count += 1
                        files_with_errors.append(f"{filename} ({split_count})")
                        st.error(f"Error splitting {filename}: {split_count}")
                
                # Complete the progress bar
                progress_bar.progress(1.0)
                progress_text.empty()
                
                # Final summary
                st.success(f"Splitting complete!")
                st.write(f"Original files processed: {processed_count}")
                st.write(f"Total split files created: {total_split_files}")
                
                # Only show file names if there are 10 or fewer
                if len(files_processed) <= 10:
                    st.write(f"Files successfully split: {', '.join(files_processed) if files_processed else 'None'}")
                else:
                    st.write(f"Files successfully split: {len(files_processed)} files")
                
                if error_count > 0:
                    with st.expander("View errors"):
                        st.warning(f"Files with errors: {error_count}")
                        st.write(f"Errors occurred in: {', '.join(files_with_errors)}")

            except Exception as e:
                st.error(f"An unexpected error occurred during splitting: {str(e)}")

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