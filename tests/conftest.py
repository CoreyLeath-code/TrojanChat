import os
import sys

# Track down the absolute directory of the tests folder
tests_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate exactly one level up to look at the project root structure
project_root = os.path.abspath(os.path.join(tests_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Handle nested tracking setups dynamically by scanning for the main app package
for root, dirs, files in os.walk(project_root):
    if "app" in dirs:
        resolved_path = os.path.abspath(root)
        if resolved_path not in sys.path:
            sys.path.insert(0, resolved_path)
