from pathlib import Path

def convert_md_to_txt(input_folder_path: str, output_folder_path: str):
    input_folder = Path(input_folder_path)
    output_folder = Path(output_folder_path)

    if not input_folder.is_dir():
        print("Invalid input folder path.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    for md_file in input_folder.glob("*.md"):
        txt_file = output_folder / (md_file.stem + ".txt")
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Converted: {md_file.name} -> {txt_file.name}")
        except Exception as e:
            print(f"Error converting {md_file.name}: {e}")

    print("All files converted and saved in:", output_folder)

if __name__ == "__main__":
    input_path = input("Enter the path to the folder containing .md files: ").strip()
    output_path = input("Enter the path to the folder where .txt files should be saved: ").strip()
    convert_md_to_txt(input_path, output_path)
