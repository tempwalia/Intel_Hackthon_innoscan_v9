'''
We can build a **robust parser** that:
- Extracts file paths
- Detects code blocks (any language)
- Creates directories automatically
- Writes files under a base folder like `project_files/`

'''

## ✅ Python Script (Robust + Production-ready)


import os
import re
from datetime import datetime

def parse_and_generate_files(input_file_path, output_base_dir="project_files"):
    """
    Parses LLM-generated code text and creates actual files in a directory structure.

    Args:
        input_file_path (str): Path to the LLM-generated text file
        output_base_dir (str): Base directory where files will be created
    """

    # Ensure base directory exists
    os.makedirs(output_base_dir, exist_ok=True)

    # Read input file
    with open(input_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to capture:
    # 1. File path from: --- FILE: path/filename.ext ---
    # 2. Code block content until next file marker or end
    pattern = re.compile(
        r"--- FILE:\s*(.*?)\s*---\n(.*?)(?=--- FILE:|$)",
        re.DOTALL
    )

    matches = pattern.findall(content)

    if not matches:
        print("⚠️ No files found. Check delimiter format.")
        return

    print(f"✅ Found {len(matches)} files to generate...\n")

    # Extract project folder name from first file path (e.g., "student_grade_calculator")
    project_folder = None
    if matches:
        first_file_path = matches[0][0].strip()
        parts = first_file_path.split('/')
        if len(parts) > 1:
            project_folder = parts[0]
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if project_folder:
        output_with_timestamp = os.path.join(output_base_dir, f"{project_folder}_{timestamp}")
    else:
        output_with_timestamp = os.path.join(output_base_dir, f"project_{timestamp}")
    
    os.makedirs(output_with_timestamp, exist_ok=True)
    print(f"📁 Output directory: {output_with_timestamp}\n")

    for file_path, code_content in matches:
        # Clean file path
        file_path = file_path.strip()

        # Final full path
        full_path = os.path.join(output_with_timestamp, file_path)

        # Create directories if not exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write file
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code_content.strip())

            print(f"✔ Created: {file_path}")

        except Exception as e:
            print(f"❌ Failed to write {file_path}: {e}")

    print(f"\n🎉 File generation completed in: {output_with_timestamp}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'code_gen', 'code', 'poc3_GENERATED_CODE.txt')
    parse_and_generate_files(input_file)