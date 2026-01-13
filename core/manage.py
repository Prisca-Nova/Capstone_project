#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Get the directory containing manage.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add this directory to Python path
sys.path.insert(0, BASE_DIR)

# If we're in a subdirectory, also add parent
parent_dir = os.path.dirname(BASE_DIR)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
