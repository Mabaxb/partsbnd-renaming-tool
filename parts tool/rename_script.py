# -*- coding: utf-8 -*-
import os
import re
import sys
import subprocess

def extract_four_digit_number(folder_name):
    """Extract the first 4-digit number from the folder name."""
    match = re.search(r'\d{4}', folder_name)
    return match.group(0) if match else None

def rename_files_in_folder(folder_path, forced_number=None):
    """
    Extract 4-digit number from folder name and replace any 4-digit numbers
    in files within the folder.
    
    Args:
        folder_path: Path to the folder to process
        forced_number: Optional 4-digit number to use instead of extracting from folder name
    """
    if not os.path.isdir(folder_path):
        print("Error: {} is not a valid directory".format(folder_path))
        return
    
    # Use provided number or extract from folder name
    if forced_number:
        extracted_number = forced_number
        folder_name = os.path.basename(folder_path)
        print("Using number {} for folder '{}'".format(extracted_number, folder_name))
    else:
        # Extract 4-digit number from folder name
        folder_name = os.path.basename(folder_path)
        extracted_number = extract_four_digit_number(folder_name)
        
        if not extracted_number:
            print("Error: No 4-digit number found in folder name: {}".format(folder_name))
            return
        
        print("Extracted number from folder '{}': {}".format(folder_name, extracted_number))
    
    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            # Rename file if it contains a 4-digit number
            original_name = file_name
            new_name = re.sub(r'\d{4}', extracted_number, original_name)
            
            if original_name != new_name:
                new_path = os.path.join(folder_path, new_name)
                try:
                    os.rename(file_path, new_path)
                    print("Renamed: {} -> {}".format(original_name, new_name))
                    file_path = new_path
                except Exception as e:
                    print("Error renaming {}: {}".format(original_name, e))
            
            # Also replace 4-digit numbers in file contents (for text files)
            try:
                _, ext = os.path.splitext(file_path)
                if ext in ['.txt', '.py', '.csv', '.json', '.md', '.xml']:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Replace 4-digit numbers in content that have the pattern [2 letters]_[char]_ before them
                    new_content = re.sub(r'([A-Za-z]{2}_[A-Za-z0-9]_)\d{4}', lambda m: m.group(1) + extracted_number, content)
                    
                    if content != new_content:
                        with open(file_path, 'w') as f:
                            f.write(new_content)
                        print("Updated content in: {}".format(new_name if original_name != new_name else original_name))
            except Exception as e:
                print("Error updating content in {}: {}".format(original_name, e))
    
    print("\nProcessing complete!")

def copy_partsbnd_files(folder_path):
    """
    Copy all .partsbnd.dcx files and add _l before the extension.
    
    Args:
        folder_path: Path to the folder to process
    """
    if not os.path.isdir(folder_path):
        print("Error: {} is not a valid directory".format(folder_path))
        return
    
    files_copied = 0
    
    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('.partsbnd.dcx'):
            # Create new filename with _l before the extension
            name_without_ext = file_name[:-len('.partsbnd.dcx')]
            new_file_name = name_without_ext + '_l.partsbnd.dcx'
            new_file_path = os.path.join(folder_path, new_file_name)
            
            try:
                # Copy the file
                with open(file_path, 'rb') as src:
                    content = src.read()
                with open(new_file_path, 'wb') as dst:
                    dst.write(content)
                print("Copied: {} -> {}".format(file_name, new_file_name))
                files_copied += 1
            except Exception as e:
                print("Error copying {}: {}".format(file_name, e))
    
    if files_copied == 0:
        print("No .partsbnd.dcx files found in {}".format(folder_path))
    else:
        print("\nCopied {} file(s)".format(files_copied))



if __name__ == "__main__":
    # Get the script's directory automatically
    parent_folder = os.path.dirname(os.path.abspath(__file__))
    print("Parent folder: {}".format(parent_folder))
    print("")
    
    print("Choose an option:")
    print("1. Process all folders in this directory")
    print("2. Use a 4-digit folder to rename its subfolders and files")
    print("3. Copy all .partsbnd.dcx files with _l suffix")
    
    choice = raw_input("Enter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        # Ask for a directory with "re_name" as default
        default_dir = os.path.join(parent_folder, "re_name")
        dir_input = raw_input("Enter directory path (default: {}): ".format(default_dir)).strip()
        
        if not dir_input:
            dir_input = default_dir
        
        if not os.path.isdir(dir_input):
            print("Error: {} is not a valid directory".format(dir_input))
        else:
            # Get all subdirectories
            subdirs = [d for d in os.listdir(dir_input) if os.path.isdir(os.path.join(dir_input, d))]
            
            if not subdirs:
                print("No subdirectories found in {}".format(dir_input))
            else:
                print("Found {} subdirectory(ies). Processing...".format(len(subdirs)))
                print("")
                
                for subdir in subdirs:
                    full_path = os.path.join(dir_input, subdir)
                    print("Processing: {}".format(subdir))
                    rename_files_in_folder(full_path)
                    print("")
    
    elif choice == "2":
        # Ask for a 4-digit number
        four_digit_input = raw_input("Enter a 4-digit number to use for renaming: ").strip()
        
        # Validate input
        if not re.match(r'^\d{4}$', four_digit_input):
            print("Error: Please enter exactly 4 digits")
        else:
            # Ask for a directory with "re_name" as default
            default_dir = os.path.join(parent_folder, "re_name")
            file_path_input = raw_input("Enter directory path (default: {}): ".format(default_dir)).strip()
            
            if not file_path_input:
                file_path_input = default_dir
            
            if not os.path.isdir(file_path_input):
                print("Error: {} is not a valid directory".format(file_path_input))
            else:
                # Get all subdirectories in the chosen path
                target_subdirs = [d for d in os.listdir(file_path_input) if os.path.isdir(os.path.join(file_path_input, d))]
                
                if not target_subdirs:
                    print("No subdirectories found in {}".format(file_path_input))
                else:
                    print("Found {} subdirectory(ies). Processing with number {}...".format(len(target_subdirs), four_digit_input))
                    print("")
                    for subdir in target_subdirs:
                        old_folder_path = os.path.join(file_path_input, subdir)
                        
                        # Rename the folder itself if it contains a 4-digit number
                        new_folder_name = re.sub(r'\d{4}', four_digit_input, subdir)
                        
                        if subdir != new_folder_name:
                            new_folder_path = os.path.join(file_path_input, new_folder_name)
                            try:
                                os.rename(old_folder_path, new_folder_path)
                                print("Renamed folder: {} -> {}".format(subdir, new_folder_name))
                                old_folder_path = new_folder_path
                            except Exception as e:
                                print("Error renaming folder {}: {}".format(subdir, e))
                        
                        # Process files in the folder
                        print("Processing files in: {}".format(new_folder_name if subdir != new_folder_name else subdir))
                        rename_files_in_folder(old_folder_path, forced_number=four_digit_input)
                        print("")
    
    elif choice == "3":
        print("Processing: {}".format(parent_folder))
        copy_partsbnd_files(parent_folder)
    
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
