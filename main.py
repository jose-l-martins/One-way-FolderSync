import os
import sys
import argparse
import time
import datetime
import shutil
import hashlib



def log(message: str, log_file_path: str):
    print(f"{message} at {datetime.datetime.now()}\n")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{message} at {datetime.datetime.now()}\n")


def sync_files_and_log(items_to_create: list, items_to_delete: list, folder_one: str, folder_two: str, log_file_path: str):
    for item in items_to_create:
        source_item_path = os.path.join(folder_one, item)
        replica_item_path = os.path.join(folder_two, item)
        if item in items_to_delete:
            shutil.copy(source_item_path, replica_item_path)
            log(f"File {replica_item_path} was modified", log_file_path)
            items_to_delete.remove(item)       
        else:            
            shutil.copy(source_item_path, replica_item_path)
            log(f"File {replica_item_path} was created", log_file_path)
                
    for item in items_to_delete:
        replica_item_path = os.path.join(folder_two, item)
        os.remove(replica_item_path)
        log(f"File {replica_item_path} was deleted", log_file_path)
        
    log(f"Sync operation cycle completed", log_file_path)
            

def scan_folder_structure(folder_path: str):
   files_paths = []
   dirs_paths = []
   
   for root, dirs, files in os.walk(folder_path):
      for name in files:
         files_paths.append(os.path.relpath(os.path.join(root, name), folder_path))
      for name in dirs:
         dirs_paths.append(os.path.relpath(os.path.join(root, name), folder_path))
            
   return files_paths, dirs_paths


def sha256_checksum(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
    return file_hash.hexdigest()


def sync_folders_and_log(source_folder_path: str, replica_folder_path: str, log_file_path: str):
    
    source_directories = scan_folder_structure(source_folder_path)[1]
    replica_directories = scan_folder_structure(replica_folder_path)[1]
    
    for directory in replica_directories:
        if directory not in source_directories:
            subdirectory_to_delete = os.path.join(replica_folder_path, directory)
            if os.path.isdir(subdirectory_to_delete):
                shutil.rmtree(subdirectory_to_delete)
                log(f"Folder {subdirectory_to_delete} was deleted", log_file_path)
                    
    for directory in source_directories:
        if directory not in replica_directories:
            subdirectory_to_create = os.path.join(replica_folder_path, directory)
            if not os.path.isdir(subdirectory_to_create):
                os.makedirs(subdirectory_to_create)
                log(f"Folder {subdirectory_to_create} was created", log_file_path)
          
    source_items = scan_folder_structure(source_folder_path)[0]
    replica_items = scan_folder_structure(replica_folder_path)[0]
    items_to_create = [item for item in source_items if item not in replica_items]
    items_to_delete = [item for item in replica_items if item not in source_items]
    items_to_checksum = [item for item in source_items if item in replica_items]
    
    if items_to_checksum != []:
        items_to_checksum_copy = list(items_to_checksum)
        for file in items_to_checksum_copy:
            if sha256_checksum(os.path.join(source_folder_path, file)) != sha256_checksum(os.path.join(replica_folder_path, file)):
                items_to_delete.append(file)
                items_to_create.append(file)
                items_to_checksum.remove(file)
            else:
                items_to_checksum.remove(file)
  
    sync_files_and_log(items_to_create, items_to_delete, source_folder_path, replica_folder_path, log_file_path)


def main():
    
    parser = argparse.ArgumentParser(description='Synchronizes all the content from a reference source folder to a replica folder, creating an exact copy, in a single direction.')
    parser.add_argument('-s','--source', help='Path to source folder', required=True)
    parser.add_argument('-r','--replica', help='Path to replica folder', required=True)
    parser.add_argument('-l','--log', help='Path to log file', required=True)
    parser.add_argument('-t','--time', help='Time interval between syncs (in seconds)', required=True)
    args = parser.parse_args()
    
    source_folder_path = args.source
    replica_folder_path = args.replica
    log_file_path = str(args.log)
    time_interval = int(args.time)
    
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