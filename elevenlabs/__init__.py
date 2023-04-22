from os import path
import sys

if __package__:
    parent_dir = path.dirname(__file__)
    root_dir = path.dirname(parent_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    if root_dir not in sys.path:
        sys.path.append(root_dir)