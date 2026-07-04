import os
import sys

# Compute the runner workspace execution point
cwd = os.path.abspath(os.path.dirname(__file__))

# Walk up or down to systematically inject the root directory context
root_dir = os.path.abspath(os.path.join(cwd, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Handle nested tracking (e.g., TrojanChat/TrojanChat parent folder duplications)
for root, dirs, files in os.walk(root_dir):
    if "app" in dirs:
        full_path = os.path.abspath(root)
        if full_path not in sys.path:
            sys.path.insert(0, full_path)
