import os
import sys
import argparse
import time
import datetime
import shutil
import hashlib


# Function to log a set of messages to a file and to the console, in a periodic manner
def log(message: str, log_file_path: str, final_message: bool = False):
    timestamp = datetime.datetime.now()
    log_entry = f"{message} at {timestamp}"
    
    if final_message:
        log_entry += "\n"

    print(f"{log_entry}")
    
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{log_entry}\n")


# Function to synchronize files between two folders and log the changes, given pre-processed lists of files to create and to delete
def sync_files_and_log(files_to_create: list, files_to_delete: list, folder_one: str, folder_two: str, log_file_path: str):
    for file in files_to_create:
        source_file_path = os.path.join(folder_one, file)
        replica_file_path = os.path.join(folder_two, file)
        # If a file is to be overwritten (deletion and then creation) with a newer version, it's present in both lists
        if file in files_to_delete:
            shutil.copy(source_file_path, replica_file_path)
            log(f"File \"{replica_file_path}\" was modified", log_file_path)
            files_to_delete.remove(file)       
        else:            
            shutil.copy(source_file_path, replica_file_path)
            log(f"File \"{replica_file_path}\" was created", log_file_path)
                
    for file in files_to_delete:
        replica_file_path = os.path.join(folder_two, file)
        os.remove(replica_file_path)
        log(f"File \"{replica_file_path}\" was deleted", log_file_path)
        
    log(f"Sync operation cycle completed", log_file_path, True)
            

# Function to scan the structure of a folder and return lists of files and subfolders
def scan_folder_structure(folder_path: str):
   files_paths = []
   dirs_paths = []
   
   for root, dirs, files in os.walk(folder_path):
      for name in files:
         files_paths.append(os.path.relpath(os.path.join(root, name), folder_path))
      for name in dirs:
         dirs_paths.append(os.path.relpath(os.path.join(root, name), folder_path))
            
   return files_paths, dirs_paths


# Function to calculate the SHA256 checksum of a file
def sha256_checksum(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
    return file_hash.hexdigest()


# Function to synchronize folders (and, thefore, both subfolder structure and the files inside) and log the changes
def sync_folders_and_log(source_folder_path: str, replica_folder_path: str, log_file_path: str):
    
    source_folders = scan_folder_structure(source_folder_path)[1]
    replica_folders = scan_folder_structure(replica_folder_path)[1]
    
    # Compare and synchronize the subfolder structure
    for folder in replica_folders:
        if folder not in source_folders:
            subfolder_to_delete = os.path.join(replica_folder_path, folder)
            if os.path.isdir(subfolder_to_delete):
                shutil.rmtree(subfolder_to_delete)
                log(f"Folder \"{subfolder_to_delete}\" was deleted", log_file_path)
                    
    for folder in source_folders:
        if folder not in replica_folders:
            subfolder_to_create = os.path.join(replica_folder_path, folder)
            if not os.path.isdir(subfolder_to_create):
                os.makedirs(subfolder_to_create)
                log(f"Folder \"{subfolder_to_create}\" was created", log_file_path)
  
    # Compare the content of the folders, first using filenames and only then using checksums, to avoid unnecessary processing
    source_files = scan_folder_structure(source_folder_path)[0]
    replica_files = scan_folder_structure(replica_folder_path)[0]
    files_to_create = [file for file in source_files if file not in replica_files]
    files_to_delete = [file for file in replica_files if file not in source_files]
    files_to_checksum = [file for file in source_files if file in replica_files]
    
    if files_to_checksum:
        for file in files_to_checksum:
            if sha256_checksum(os.path.join(source_folder_path, file)) != sha256_checksum(os.path.join(replica_folder_path, file)):
                files_to_delete.append(file)
                files_to_create.append(file)
  
    sync_files_and_log(files_to_create, files_to_delete, source_folder_path, replica_folder_path, log_file_path)


def main():
    
    parser = argparse.ArgumentParser(description='Synchronizes all the content from a reference source folder to a replica folder, creating an exact copy, in a single direction.')
    parser.add_argument('-s','--source', help='Path to source folder', required=True)
    parser.add_argument('-r','--replica', help='Path to replica folder', required=True)
    parser.add_argument('-l','--log', help='Path to log file', required=True)
    parser.add_argument('-t','--time', help='Time interval between syncs (in seconds)', required=True)
    args = parser.parse_args()
    
    source_folder_path = args.source
    replica_folder_path = args.replica
    log_file_path = args.log
    time_interval = int(args.time)
    
    # Check if source and replica folders exist
    if not os.path.exists(source_folder_path):
        print(f"ERROR: Source folder '{source_folder_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(replica_folder_path):
        print(f"ERROR: Replica folder '{replica_folder_path}' does not exist.")
        sys.exit(1)
    
    try:
        while True:
            print("STATUS: Beginning sync operation. Avoid interrupting the script, until further notice, to prevent data loss or corruption.\n")
            sync_folders_and_log(source_folder_path, replica_folder_path, log_file_path)
            print("STATUS: You may now interrupt the script, safely.\n")
            time.sleep(time_interval)

    except KeyboardInterrupt:
        print("\nSTATUS: Script interrupted. Exiting.")
        sys.exit(0)
    

if __name__ == "__main__":
    main()