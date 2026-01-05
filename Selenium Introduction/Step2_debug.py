import os

# Check if HTML file exists
html_file = "index.html"
if os.path.exists(html_file):
    print(f"✓ HTML file found: {os.path.abspath(html_file)}")
    print(f"  File size: {os.path.getsize(html_file)} bytes")
else:
    print(f"✗ HTML file not found: {html_file}")
    print("Please copy the HTML report from Podman container to this directory")