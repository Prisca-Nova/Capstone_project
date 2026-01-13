import os
import sys

print("=== FINAL FIX ===\n")

# Get current directory
current_dir = os.getcwd()
print(f"Working in: {current_dir}")

# List what we have
print("\nCurrent files:")
for item in os.listdir(current_dir):
    item_path = os.path.join(current_dir, item)
    if os.path.isdir(item_path):
        print(f"📁 {item}/")
    else:
        print(f"📄 {item}")

# Check for settings.py location
print("\nLooking for settings.py...")
if os.path.exists('settings.py'):
    print("✓ Found settings.py in current directory")
    settings_location = 'core.settings'
elif os.path.exists('core/settings.py'):
    print("✓ Found settings.py in core/ directory")
    settings_location = 'core.core.settings'
else:
    print("✗ Could not find settings.py!")
    # Search for it
    for root, dirs, files in os.walk('.'):
        if 'settings.py' in files:
            print(f"Found settings.py at: {root}/settings.py")
            rel_path = os.path.relpath(root, current_dir).replace('\\', '.').replace('/', '.')
            if rel_path == '.':
                settings_location = 'core.settings'
            else:
                settings_location = f'{rel_path}.settings'
            break

print(f"\nSettings module will be: {settings_location}")

# Create the definitive manage.py
print("\nCreating definitive manage.py...")
manage_content = f'''#!/usr/bin/env python
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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{settings_location}')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''

with open('manage.py', 'w') as f:
    f.write(manage_content)

print("✓ Created manage.py")

# Create __init__.py files if missing
print("\nCreating __init__.py files...")
init_created = []

# Check for core directory
if os.path.exists('core') and os.path.isdir('core'):
    init_file = os.path.join('core', '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Django core package\n')
        init_created.append('core/__init__.py')

# Check for api directory
if os.path.exists('api') and os.path.isdir('api'):
    init_file = os.path.join('api', '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# API app package\n')
        init_created.append('api/__init__.py')

if init_created:
    print(f"Created: {', '.join(init_created)}")
else:
    print("All __init__.py files exist")

# Test the import
print("\nTesting import...")
try:
    # Add current directory to path for testing
    sys.path.insert(0, current_dir)
    
    if settings_location == 'core.settings':
        import core
        print("✓ Successfully imported 'core'")
        from core import settings
        print("✓ Successfully imported 'core.settings'")
    elif settings_location == 'core.core.settings':
        import core.core
        print("✓ Successfully imported 'core.core'")
        from core.core import settings
        print("✓ Successfully imported 'core.core.settings'")
    
    print("\n🎉 SUCCESS! All imports work.")
    
except ImportError as e:
    print(f"\n✗ Import failed: {e}")
    print("\nTrying alternative approach...")
    
    # Try direct import
    try:
        import importlib.util
        
        if settings_location == 'core.settings':
            spec = importlib.util.spec_from_file_location("settings", "settings.py")
        elif settings_location == 'core.core.settings':
            spec = importlib.util.spec_from_file_location("settings", "core/settings.py")
        
        if spec:
            settings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings_module)
            print("✓ Direct import of settings.py successful")
    except Exception as e2:
        print(f"✗ Direct import also failed: {e2}")

print("\n" + "="*50)
print("FINAL INSTRUCTIONS:")
print("1. Run: python manage.py makemigrations")
print("2. Run: python manage.py migrate")
print("3. Run: python manage.py createsuperuser")
print("4. Run: python manage.py runserver")
print("\nIf you still get 'No module named core' error, run this:")
print("python -c \"import sys; print('\\n'.join(sys.path))\"")
print("\nYour server will run at: http://localhost:8000")