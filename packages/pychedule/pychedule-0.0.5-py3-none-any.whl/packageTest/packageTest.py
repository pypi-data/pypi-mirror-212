import os
import subprocess
import argparse

def load_python_files(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths

def execute_python_files(file_paths):
    for file_path in file_paths:
        subprocess.run(["python", file_path])
        
