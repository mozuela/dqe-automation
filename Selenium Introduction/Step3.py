# STEP 3: Test loading the HTML report
import os
import time

# Use what already works - direct Chrome
from selenium import webdriver

print("STEP 3: Testing if we can load the HTML report")
print("=" * 50)

# Check file
html_file = "report.html"
if not os.path.exists(html_file):
    print(f"ERROR: {html_file} not found")
    exit(1)

file_url = f"file://{os.path.abspath(html_file)}"
print(f"File: {html_file}")
print(f"URL: {file_url}")

try:
    # SIMPLE: Just create driver like the test that worked
    print("\nCreating Chrome driver...")
    driver = webdriver.Chrome()

    print("SUCCESS: Driver created")

    # Load the page
    print(f"\nLoading {file_url}...")
    driver.get(file_url)

    # Wait
    time.sleep(3)

    print(f"\nPage loaded!")
    print(f"Title: {driver.title}")

    # Take screenshot
    screenshot_name = "step3_loaded.png"
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot saved: {screenshot_name}")

    # Count some elements
    tables = driver.find_elements("tag name", "table")
    print(f"Tables found: {len(tables)}")

    # Close
    driver.quit()
    print("\nDone! Check step3_loaded.png")

except Exception as e:
    print(f"\nERROR: {e}")