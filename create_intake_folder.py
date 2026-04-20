import os

def create_folders():
    folders = ["intake_queue", "media"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
        else:
            print(f"Folder already exists: {folder}")

if __name__ == "__main__":
    create_folders()
