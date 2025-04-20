import os
import shutil

def move_fact_sheet_pdfs(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Loop through all files in the source directory
    for filename in os.listdir(source_dir):
        # Full path of the file
        source_path = os.path.join(source_dir, filename)

        # Check if it's a file and matches our criteria
        if os.path.isfile(source_path) and filename.endswith(".pdf") and "Fact_Sheet" in filename:
            destination_path = os.path.join(destination_dir, filename)

            # Move the file
            shutil.move(source_path, destination_path)
            print(f"Moved: {filename}")

if __name__ == "__main__":
    # Set your source and destination directories
    source_directory = "./downloadedPDFs"
    destination_directory = "./fact_sheets"
    
    move_fact_sheet_pdfs(source_directory, destination_directory)
