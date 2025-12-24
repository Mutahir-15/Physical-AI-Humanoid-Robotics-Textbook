import os
import glob

base_dir = r"F:\\Github\\spec-driven-online-hackathon-1"
output_file = os.path.join(base_dir, "backend", "data", "book.md")
docs_dir = os.path.join(base_dir, "docs")

filtered_content = []

# Get all .mdx files recursively in the docs directory
mdx_files = glob.glob(os.path.join(docs_dir, "**", "*.mdx"), recursive=True)

for file_path in mdx_files:
    # Normalize path to use forward slashes for consistent comparison
    normalized_file_path = file_path.replace(os.sep, '/')
    
    # Check if the file belongs to a 'moduleX' directory
    if "docs/module" in normalized_file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            filtered_content.append(content)
            filtered_content.append("\n\n") # Add some separation between files

# Write the filtered content to book.md
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("".join(filtered_content))
    print(f"Successfully wrote filtered content to {output_file}")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")
