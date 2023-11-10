# One-way-FolderSync (Folder Synchronization Program)

This Python program provides a simple yet powerful way to synchronize the content of two folders, maintaining an exact copy in a single direction. It includes features such as file modification tracking, checksum verification and periodic synchronization.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Options](#options)
- [Example](#example)

## Features

- **Lightweight and Dependency-Free:** This synchronization script is designed to be lightweight and does not require any external dependencies. It relies solely on standard Python libraries, making it easy to use and deploy without additional setup.

- **File Synchronization:** Keeps the content of a replica folder in sync with a source folder, creating an exact copy in a single direction.

- **Folder Structure Synchronization:** Maintains the subfolder structure of the replica folder to match the source folder.

- **Periodic Sync:** Automatically performs synchronization at specified time intervals, allowing for hands-free operation.

- **Logging:** Logs detailed information about the synchronization process, including file creations, modifications and deletions, to a specified log file and the command line.

- **Checksum Verification:** Ensures the integrity of files by verifying their SHA256 checksums, avoiding unnecessary file operations. SHA256 is an industry standard and is collision-resistant.

- **Interrupt Handling:** Allows safer interruption of the script and helps avoid data loss or corruption. Warns about the indicated time window for manual user interruption.

- **User-Friendly Command Line Interface:** Simple and intuitive command line options for easy configuration.





## Prerequisites

- Python 3.x
- Standard libraries: `os`, `sys`, `argparse`, `time`, `datetime`, `shutil`, `hashlib`

## Usage

```bash
python main.py -s SOURCE_FOLDER -r REPLICA_FOLDER -l LOG_FILE -t TIME_INTERVAL
```

## Options

- `-s, --source`: Path to the source folder.
- `-r, --replica`: Path to the replica folder.
- `-l, --log`: Path to the log file.
- `-t, --time`: Time interval between syncs (in seconds).

## Example

```bash
python main.py -s /path/to/source -r /path/to/replica -l /path/to/log.txt -t 3600
```

This example synchronizes the content from `/path/to/source` to `/path/to/replica` every hour (3600 seconds), with log entries recorded in `/path/to/log.txt`.