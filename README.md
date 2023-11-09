# Folder Synchronization Program

This Python program synchronizes two folders, referred to as the "source" and "replica." The goal is to maintain an identical copy of the source folder within the replica folder. The synchronization is one-way, ensuring that the content of the replica folder is modified to precisely match the content of the source folder. The synchronization process is performed periodically.

## Features

- One-way synchronization: replica folder is updated to mirror the content of the source folder.
- Periodic synchronization intervals, allowing the replica to continuously be up-to-date.
- File creation, copying and removal operations are logged to a log file and console output.
- Specification of folder paths, synchronization interval and log file path, via command line arguments.
- Avoidance of third-party libraries for folder synchronization (which would be redundant and defeat the purpose), while allowing the use of external libraries for other simpler, well-known algorithms.
