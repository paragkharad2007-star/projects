import shutil
from pathlib import Path

# ---------------- SETTINGS ----------------
DRY_RUN = False  # True = print only, False = move files

# Target folder on Desktop
TARGET_DIR = Path.home() / "parag_ok"

# File categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Music": [".mp3", ".wav"],
    "Videos": [".mp4", ".mkv"],
    "Archives": [".zip", ".rar"],
}
# ------------------------------------------

def organize_files():
    # Create target folder automatically
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📂 Target folder being used: {TARGET_DIR}")

    files_found = False

    for file in TARGET_DIR.iterdir():
        if file.is_file():
            files_found = True
            moved = False

            for folder, extensions in FILE_TYPES.items():
                if file.suffix.lower() in extensions:
                    destination_folder = TARGET_DIR / folder
                    destination_folder.mkdir(exist_ok=True)
                    destination = destination_folder / file.name

                    if DRY_RUN:
                        print(f"[DRY RUN] {file.name} → {folder}")
                    else:
                        shutil.move(str(file), str(destination))
                        print(f"[MOVED] {file.name} → {folder}")

                    moved = True
                    break

            if not moved:
                other_folder = TARGET_DIR / "Others"
                other_folder.mkdir(exist_ok=True)
                destination = other_folder / file.name

                if DRY_RUN:
                    print(f"[DRY RUN] {file.name} → Others")
                else:
                    shutil.move(str(file), str(destination))
                    print(f"[MOVED] {file.name} → Others")

    if not files_found:
        print("⚠ No files found in target folder.")

if __name__ == "__main__":
    print("File Organizer Started (Windows)")
    print("DRY RUN MODE:", DRY_RUN)
    print("-" * 40)
    organize_files()
    print("-" * 40)
    print("Done.")
