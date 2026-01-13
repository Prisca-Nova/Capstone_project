import os
import shutil

print("Fixing Django project structure...")

# Check current location
if os.path.exists('core/core'):
    print("Found nested core directory. Fixing...")
    
    # Move everything from core/core/ to core/
    for item in os.listdir('core/core'):
        src = os.path.join('core/core', item)
        dst = os.path.join('core', item)
        if os.path.exists(dst):
            print(f"  Skipping {item} - already exists")
        else:
            shutil.move(src, dst)
            print(f"  Moved {item}")
    
    # Remove empty core/core directory
    os.rmdir('core/core')
    
    print("Structure fixed!")
    
    # Update manage.py
    manage_py = """#!/usr/bin/env python
\"\"\"Django's command-line utility for administrative tasks.\"\"\"
import os
import sys

def main():
    \"\"\"Run administrative tasks.\"\"\"
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
    """
    
    with open('core/manage.py', 'w') as f:
        f.write(manage_py)
    
    print("Updated manage.py")
    print("\nNow run these commands:")
    print("cd core")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print("python manage.py createsuperuser")
    print("python manage.py runserver")
else:
    print("Structure looks correct already.")
    print("Make sure manage.py contains: os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')")