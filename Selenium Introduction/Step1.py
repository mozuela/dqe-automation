import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_prerequisites():
    """Check if all prerequisites are met"""
    print("\n" + "=" * 60)
    print("PREREQUISITE CHECK - Selenium Homework")
    print("=" * 60)

    # Check current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    # List files in current directory
    print("\nFiles in current directory:")
    files = os.listdir('.')
    for file in files:
        print(f"  - {file}")

    # Check for HTML report (try different names)
    html_files = []
    for file in files:
        if file.endswith('.html'):
            html_files.append(file)

    if html_files:
        print(f"\n✓ Found HTML file(s): {html_files}")
        # Use the first HTML file found
        html_file = html_files[0]
        print(f"  Using: {html_file}")
        print(f"  Full path: {os.path.abspath(html_file)}")
        print(f"  Size: {os.path.getsize(html_file)} bytes")
        return html_file
    else:
        print("\n✗ No HTML files found in current directory")
        print("  Please ensure you have copied the HTML report from Podman")
        print("  Expected: .html file in current directory")
        return None


def inspect_html_file(html_file):
    """Quickly inspect the HTML file"""
    print("\n" + "=" * 60)
    print("HTML FILE INSPECTION")
    print("=" * 60)

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"File: {html_file}")
        print(f"Size: {len(content)} characters")

        # Check for common elements
        checks = {
            'Has <table> tag': '<table' in content.lower(),
            'Has chart references': any(word in content.lower() for word in ['chart', 'doughnut', 'canvas', 'svg']),
            'Has filter references': 'filter' in content.lower(),
            'Has JavaScript': '<script' in content.lower(),
        }

        print("\nContent analysis:")
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")

        # Get first few lines to see structure
        print("\nFirst 5 lines:")
        lines = content.split('\n')[:5]
        for i, line in enumerate(lines, 1):
            print(f"  {i}: {line[:100]}..." if len(line) > 100 else f"  {i}: {line}")

        return True

    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return False


if __name__ == "__main__":
    html_file = check_prerequisites()

    if html_file:
        print("\n" + "=" * 60)
        print("STEP 1 COMPLETE: HTML file verified")
        print("=" * 60)

        # Inspect the HTML file
        inspect_html_file(html_file)

        print("\n" + "=" * 60)
        print("NEXT STEP: Create the context manager")
        print("=" * 60)
    else:
        print("\n✗ Cannot proceed without HTML file")