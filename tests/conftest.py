import os
import sys

# Get the absolute directory where this conftest.py file lives
current_dir = os.path.dirname(os.path.abspath(__file__))

# Map one level up to check the root project path context
root_project_path = os.path.abspath(os.path.join(current_dir, ".."))
if root_project_path not in sys.path:
    sys.path.insert(0, root_project_path)

# Systematically search downstream folders to handle nested folder structures
for root, dirs, files in os.walk(root_project_path):
    if "app" in dirs:
        target_path = os.path.abspath(root)
        if target_path not in sys.path:
            sys.path.insert(0, target_path)
