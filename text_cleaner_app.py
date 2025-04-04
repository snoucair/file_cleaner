import streamlit as st
import os
from tkinter import filedialog
import tkinter as tk
import re

def is_line_valid(line):
    # Allow lines starting with P1 or P2
    if line.strip().startswith(('P1', 'P2')):
        return True
    
    # Define allowed characters (letters, numbers, and specific special characters)
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-_:;,.=/\\*()\t \n')
    
    # Check if all characters in the line are allowed
    return all(char in allowed_chars for char in line)

def process_file(input_file, output_file):
    lines_removed = 0
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fallback to a more lenient encoding if UTF-8 fails
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    
    # Filter lines and count removed ones
    filtered_lines = []
    for line in lines:
        if is_line_valid(line):
            filtered_lines.append(line)
        else:
            lines_removed += 1
    
    # Write filtered content to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)
    
    return lines_removed

def main():
    st.title("Text Cleaner")
    st.write("Clean text files by removing lines with non-standard characters while preserving specific patterns.")
    
    # Initialize tkinter root window but hide it
    root = tk.Tk()
    root.withdraw()
    
    # Input folder selection
    if st.button("Select Input Folder"):
        input_folder = filedialog.askdirectory()
        if input_folder:
            st.session_state.input_folder = input_folder
            st.write(f"Selected input folder: {input_folder}")
    
    # Output folder selection
    if st.button("Select Output Folder"):
        output_folder = filedialog.askdirectory()
        if output_folder:
            st.session_state.output_folder = output_folder
            st.write(f"Selected output folder: {output_folder}")
    
    # Process files button
    if st.button("Process Files"):
        if not hasattr(st.session_state, 'input_folder') or not hasattr(st.session_state, 'output_folder'):
            st.error("Please select both input and output folders first.")
            return
        
        input_folder = st.session_state.input_folder
        output_folder = st.session_state.output_folder
        
        files_processed = 0
        total_lines_removed = 0
        errors = []
        
        # Process each file in the input folder
        for filename in os.listdir(input_folder):
            try:
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)
                
                if os.path.isfile(input_path):
                    lines_removed = process_file(input_path, output_path)
                    files_processed += 1
                    total_lines_removed += lines_removed
            except Exception as e:
                errors.append(f"Error processing {filename}: {str(e)}")
        
        # Display results
        st.success(f"Processing complete!\nFiles processed: {files_processed}\nTotal lines removed: {total_lines_removed}")
        if errors:
            st.error("Errors encountered:")
            for error in errors:
                st.write(error)

if __name__ == "__main__":
    main()
```