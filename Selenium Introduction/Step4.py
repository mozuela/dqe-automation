# STEP 4: Extract table data from SVG elements
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("STEP 4: Extracting table data from SVG")
print("=" * 60)

driver = webdriver.Chrome()
driver.get(f"file://{os.path.abspath('report.html')}")
time.sleep(5)

# Create output directory
os.makedirs("csv_files", exist_ok=True)

# STRATEGY: Extract data from SVG text elements
print("\n1. Finding all text elements in the table area...")

# Find SVG elements that contain the table
svg_elements = driver.find_elements(By.TAG_NAME, "svg")
print(f"Found {len(svg_elements)} SVG elements")

# Look for the main table SVG (largest one)
main_svg = None
for svg in svg_elements:
    size = svg.size
    if size['width'] > 900 and size['height'] > 700:  # Main chart/table area
        main_svg = svg
        print(f"Found main SVG: {size['width']}x{size['height']}")
        break

if not main_svg:
    print("❌ Could not find main SVG")
    driver.quit()
    exit(1)

# 2. Extract text elements with different locators
print("\n2. Extracting text elements using multiple locators...")

# METHOD 1: Find by class name 'cell-text'
table_data = {}
try:
    cell_texts = main_svg.find_elements(By.CSS_SELECTOR, "text.cell-text")
    print(f"  Method 1 (CSS .cell-text): Found {len(cell_texts)} elements")

    for elem in cell_texts:
        text = elem.text.strip()
        if text:
            # Get position for sorting
            location = elem.location
            table_data[f"{location['y']}_{location['x']}"] = {
                'text': text,
                'x': location['x'],
                'y': location['y'],
                'element': elem
            }
except Exception as e:
    print(f"  Method 1 error: {e}")

# METHOD 2: Find all text elements in SVG
if len(table_data) < 10:  # If not enough data
    try:
        all_texts = main_svg.find_elements(By.TAG_NAME, "text")
        print(f"  Method 2 (tag text): Found {len(all_texts)} text elements")

        for elem in all_texts:
            text = elem.text.strip()
            if text and len(text) > 1:  # Skip single characters
                location = elem.location
                key = f"{location['y']}_{location['x']}"
                if key not in table_data:
                    table_data[key] = {
                        'text': text,
                        'x': location['x'],
                        'y': location['y'],
                        'element': elem
                    }
    except Exception as e:
        print(f"  Method 2 error: {e}")

# METHOD 3: Find by XPath for specific text patterns
try:
    # Look for facility types
    facility_xpaths = [
        "//text[contains(@class, 'cell-text') and (text()='Clinic' or text()='Hospital' or text()='Specialty Center')]",
        "//tspan[text()='Clinic' or text()='Hospital' or text()='Specialty Center']",
        "//text[text()='Facility Type' or text()='Visit Date' or text()='Average Time Spent']"
    ]

    for xpath in facility_xpaths:
        elements = driver.find_elements(By.XPATH, xpath)
        if elements:
            print(f"  Method 3 (XPath): Found {len(elements)} with '{xpath[:50]}...'")
            for elem in elements:
                text = elem.text.strip()
                if text:
                    location = elem.location
                    key = f"{location['y']}_{location['x']}"
                    if key not in table_data:
                        table_data[key] = {
                            'text': text,
                            'x': location['x'],
                            'y': location['y'],
                            'element': elem
                        }
except Exception as e:
    print(f"  Method 3 error: {e}")

print(f"\nTotal unique text elements collected: {len(table_data)}")

# 3. Organize data into table structure
print("\n3. Organizing data into table rows...")

# Sort by Y position (rows), then X position (columns)
sorted_items = sorted(table_data.items(), key=lambda x: (x[1]['y'], x[1]['x']))

# Group by Y position to find rows
rows = {}
for key, data in sorted_items:
    y = data['y']
    if y not in rows:
        rows[y] = []
    rows[y].append(data)

print(f"Found {len(rows)} potential rows")

# Convert to table structure
table_rows = []
for y_pos in sorted(rows.keys()):
    row_data = rows[y_pos]
    # Sort cells in this row by X position
    row_data.sort(key=lambda x: x['x'])
    row_texts = [cell['text'] for cell in row_data]
    table_rows.append(row_texts)

# 4. Identify headers and data
print("\n4. Identifying table structure...")

headers = ['Facility Type', 'Visit Date', 'Average Time Spent']
data_rows = []

# Look for header row
header_found = False
for i, row in enumerate(table_rows):
    if 'Facility Type' in ' '.join(row) or 'Visit Date' in ' '.join(row):
        print(f"  Header row {i}: {row}")
        # Update headers from actual data if available
        if len(row) >= 3:
            headers = row[:3]
        header_found = True
    elif header_found and len(row) >= 3:
        # This is a data row (after headers)
        # Check if it looks like data (has facility type and date/number)
        row_text = ' '.join(row)
        if any(facility in row_text for facility in ['Clinic', 'Hospital', 'Specialty Center']):
            data_rows.append(row[:3])  # Take first 3 columns
            print(f"  Data row {len(data_rows)}: {row[:3]}")

# Alternative: If no headers found, look for data patterns
if not header_found:
    print("  No headers found, looking for data patterns...")
    for row in table_rows:
        row_text = ' '.join(row)
        # Look for rows with facility types and numbers
        if (any(facility in row_text for facility in ['Clinic', 'Hospital', 'Specialty Center']) and
                any(char.isdigit() for char in row_text)):
            if len(row) >= 3:
                data_rows.append(row[:3])
                print(f"  Data row {len(data_rows)}: {row[:3]}")

print(f"\nFound {len(data_rows)} data rows")

# 5. Save to CSV
if data_rows:
    csv_filename = "csv_files/table.csv"

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write headers
        writer.writerow(headers)

        # Write data
        for row in data_rows:
            writer.writerow(row)

    print(f"\n✅ SUCCESS: Saved {len(data_rows)} rows to {csv_filename}")

    # Show sample
    print("\nSample of extracted data:")
    print(f"Headers: {headers}")
    for i, row in enumerate(data_rows[:5]):
        print(f"Row {i + 1}: {row}")
else:
    print("\n❌ No data rows could be extracted")

    # Save headers only
    csv_filename = "csv_files/table.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

    print(f"Created CSV with headers only: {csv_filename}")

# 6. Take screenshot of the table area
try:
    # Get the table area
    if table_data:
        min_x = min(data['x'] for data in table_data.values())
        max_x = max(data['x'] for data in table_data.values())
        min_y = min(data['y'] for data in table_data.values())
        max_y = max(data['y'] for data in table_data.values())

        width = max_x - min_x + 100
        height = max_y - min_y + 100

        # Create a screenshot of the table area
        driver.save_screenshot("table_area.png")
        print(f"\n📸 Table area screenshot: table_area.png")
except:
    pass

driver.quit()

print("\n" + "=" * 60)
print("STEP 4 COMPLETED")
print("=" * 60)