import os
import hashlib
import time

# Function to compute the hash of a file
def compute_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Function to check if the hash is present in the blacklist
def check_blacklist(hash_value, blacklist):
    with open(blacklist, 'r') as f:
        for line in f:
            if line.strip() == hash_value:
                return True
    return False

# Function to monitor the Downloads directory for new files
# Function to monitor the Downloads directory for new files and subdirectories
def monitor_downloads_directory(downloads_dir, blacklist):
    files_dict = {}
    while True:
        for root, dirs, files in os.walk(downloads_dir):
            for file_name in files:
                 if file_name.endswith('.exe'):  
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path):
                        if file_name not in files_dict:
                            print(f"New file detected: {file_name}")
                            hash_value = compute_hash(file_path)
                            files_dict[file_name] = hash_value
                            if check_blacklist(hash_value, blacklist):
                                print(f"Warning: File '{file_name}' is a potential Cryptojacking executable.")
                        else:
                            current_hash = compute_hash(file_path)
                            if current_hash != files_dict[file_name]:
                                print(f"Hash mismatch for file: {file_name}")
                                print(f"Old Hash: {files_dict[file_name]}")
                                print(f"New Hash: {current_hash}")
                                files_dict[file_name] = current_hash
                                if check_blacklist(current_hash, blacklist):
                                    print(f"Warning: File '{file_name}' is a potential Cryptojacking executable.")
        time.sleep(10)  # Check every 10 seconds

# Usage example:
downloads_directory = r'C:\Users\jacks\Downloads'
blacklist = 'blacklist.txt'
monitor_downloads_directory(downloads_directory, blacklist)
