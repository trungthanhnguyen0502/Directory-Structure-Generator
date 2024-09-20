import os
import argparse

special_files = ["Dockerfile"]
indent_nb = 4


def create_structure_from_txt(file_path, save_dir):
    with open(file_path, "r") as f:
        lines = f.readlines()

    current_path = []
    for line in lines:
        # Strip the line of extra spaces and newlines
        stripped_line = line
        if not stripped_line.strip():
            break
        if stripped_line.strip() == ".":
            continue

        # Remove trailing comments (everything after '#')
        stripped_line = (
            stripped_line.replace("│", " ")
            .replace("├", " ")
            .replace("─", " ")
            .replace("└", " ")
            .lstrip()
        )
        # Get indentation level (each indentation corresponds to 4 spaces)
        level = (len(line) - len(stripped_line)) // indent_nb
        if not stripped_line:  # Skip empty lines
            continue

        stripped_line = stripped_line.split("#")[0].strip().replace("/", "")

        if "." not in stripped_line and stripped_line not in special_files:
            # Update the current path based on indentation level
            current_path = current_path[:level]  # Adjust to the correct level
            current_path.append(stripped_line)
            dir_path = os.path.join(save_dir, *current_path)

            # Create the directory if it doesn't exist
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"Created directory: {dir_path} at level {level}")

        # If it's a file
        elif stripped_line:
            current_path = current_path[:level]  # Adjust to the correct level
            file_path = os.path.join(save_dir, *current_path, stripped_line)

            # Create the file
            if not os.path.exists(file_path):
                with open(file_path, "w") as fp:
                    pass  # Create an empty file
                print(f"Created file: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create directory and file structure from a text file."
    )
    parser.add_argument(
        "--structure_txt",
        type=str,
        help="Path to the directory structure text file.",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        help="Path to the directory where the structure will be created.",
    )

    args = parser.parse_args()

    create_structure_from_txt(args.structure_txt, args.save_dir)


if __name__ == "__main__":
    main()
