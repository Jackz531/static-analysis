import os
import hashlib
import time
import zipfile

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

# Function to monitor the Downloads directory for new executable files
def monitor_executables_directory(downloads_dir, blacklist):
    files_dict = {}
    while True:
        for root, dirs, files in os.walk(downloads_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path) and file_name.endswith('.exe'):
                    if file_name not in files_dict:
                        print(f"New executable detected: {file_name}")
                        hash_value = compute_hash(file_path)
                        files_dict[file_name] = hash_value
                        if check_blacklist(hash_value, blacklist):
                            print(f"Warning: File '{file_name}' is a potential Cryptojacking executable.")
                    else:
                        current_hash = compute_hash(file_path)
                        if current_hash != files_dict[file_name]:
                            print(f"Hash mismatch for executable: {file_name}")
                            print(f"Old Hash: {files_dict[file_name]}")
                            print(f"New Hash: {current_hash}")
                            files_dict[file_name] = current_hash
                            if check_blacklist(current_hash, blacklist):
                                print(f"Warning: File '{file_name}' is a potential Cryptojacking executable.")
                                #delte reported file from folder
                                os.remove(file_path)


        

        time.sleep(10)  # Check every 10 seconds
def get_downloads_folder():
    # Get the user's home directory
    home_directory = os.path.expanduser("~")
    
    # Construct the Downloads folder path
    downloads_folder = os.path.join(home_directory, "Downloads")
    
    return downloads_folder
# Usage example:
downloads_directory = get_downloads_folder()
blacklist = 'blacklist.txt'
monitor_executables_directory(downloads_directory, blacklist)
