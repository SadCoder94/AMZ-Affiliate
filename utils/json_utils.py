"""
JSON Utilities Module
Provides functions for formatting and managing JSON files in the project.
"""

import json
from pathlib import Path

def beautify_json_files(directory: str, indent: int = 4):
    """
    Beautifies all JSON files in the specified directory by reformatting them with proper indentation.

    Args:
        directory (str): Path to the directory containing JSON files.
        indent (int): Number of spaces for indentation (default: 4).
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Directory {directory} does not exist.")
        return

    for file_path in dir_path.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent)
            print(f"Beautified {file_path}")
        except Exception as e:
            print(f"Error beautifying {file_path}: {e}")

def beautify_json_file(file_path: str, indent: int = 4):
    """
    Beautifies a single JSON file by reformatting it with proper indentation.

    Args:
        file_path (str): Path to the JSON file.
        indent (int): Number of spaces for indentation (default: 4).
    """
    path = Path(file_path)
    if not path.exists():
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        print(f"Beautified {file_path}")
    except Exception as e:
        print(f"Error beautifying {file_path}: {e}")

if __name__ == "__main__":
    # Run beautification on cache directories
    beautify_json_files("scraper_cache")
    beautify_json_files("scripts_cache")