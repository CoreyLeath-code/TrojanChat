import os
import sys

# Dynamically find the project root folder context
# and inject it directly into the system search path arrays
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
