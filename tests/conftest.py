import os
import sys

# Dynamically compute the absolute path of the root repository directory
# and append it directly to sys.path before pytest collects modules.
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
