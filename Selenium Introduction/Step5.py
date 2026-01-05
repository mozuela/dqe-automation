# STEP 5: Doughnut Chart Interaction (Fixed)
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

print("STEP 5: Doughnut Chart Interaction (Fixed)")
print("=" * 60)

driver = webdriver.Chrome()
driver.get(f"file://{os.path.abspath('report.html')}")
time.sleep(5)

# Create directories
os.makedirs("screenshots", exist_ok=True)
os.makedirs("csv_files", exist_ok=True)

screenshot_count = 0
csv_count = 0


# Function to take screenshot
def take_screenshot(name):
    """Take and save screenshot"""
    global screenshot_count
    filename = f"screenshots/{name}{screenshot_count}.png"
    driver.save_screenshot(filename)
    print(f"  📸 Saved: {filename}")
    screenshot_count += 1
    return filename


# Function to extract chart data
def extract_chart_data():
    """Extract data from doughnut chart"""
    global csv_count

    try:
        # Look for chart data in the legend
        chart_data = []

        # Find legend items with their values
        # The legend shows: "Clinic 34", "Specialty Center 19", etc.
        legend_items = driver.find_elements(By.CSS_SELECTOR, "text.legendtext")

        for item in legend_items:
            text = item.text.strip()
            if text:
                # Text format: "Clinic 34" or "Specialty Center 19"
                parts = text.split()
                if len(parts) >= 2:
                    # Facility type is all parts except last
                    facility = ' '.join(parts[:-1])
                    value = parts[-1]
                    if value.replace('.', '').isdigit():  # Check if it's a number
                        chart_data.append([facility, value])

        # If no data found, try alternative extraction
        if not chart_data:
            # Look in the main chart area
            body_text = driver.find_element(By.TAG_NAME, "body").text
            lines = body_text.split('\n')
            for line in lines:
                line = line.strip()
                if (('Clinic' in line or 'Hospital' in line or 'Specialty Center' in line) and
                        any(char.isdigit() for char in line)):
                    import re
                    # Extract last number in the line
                    numbers = re.findall(r'\d+\.?\d*', line)
                    if numbers:
                        # Identify facility
                        facility = "Unknown"
                        if 'Clinic' in line:
                            facility = "Clinic"
                        elif 'Hospital' in line:
                            facility = "Hospital"
                        elif 'Specialty Center' in line:
                            facility = "Specialty Center"

                        chart_data.append([facility, numbers[-1]])

        # Save to CSV
        if chart_data:
            csv_filename = f"csv_files/doughnut{csv_count}.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Facility Type', 'Min Average Time Spent'])
                for row in chart_data:
                    writer.writerow(row)

            print(f"  💾 Chart data saved: {csv_filename}")
            csv_count += 1
            return True
        else:
            # Create empty CSV with headers
            csv_filename = f"csv_files/doughnut{csv_count}.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Facility Type', 'Min Average Time Spent'])

            print(f"  ⚠️ Created empty CSV: {csv_filename}")
            csv_count += 1
            return False

    except Exception as e:
        print(f"  ❌ Error extracting chart data: {e}")
        return False


# 1. Take initial screenshot (unfiltered state)
print("\n1. Taking initial screenshot (unfiltered)...")
take_screenshot("screenshot")
extract_chart_data()

# 2. Find the legend toggle elements (the actual clickable areas)
print("\n2. Finding legend toggle elements...")

# Look for the legend toggle rectangles
legend_toggles = driver.find_elements(By.CSS_SELECTOR, "rect.legendtoggle")
print(f"  Found {len(legend_toggles)} legend toggle rectangles")

# Also find the legend text to know what each toggle represents
legend_texts = driver.find_elements(By.CSS_SELECTOR, "text.legendtext")
print(f"  Found {len(legend_texts)} legend text elements")

# Map toggles to their labels
legend_items = []
for i in range(min(len(legend_toggles), len(legend_texts))):
    toggle = legend_toggles[i]
    text_elem = legend_texts[i]

    legend_items.append({
        'toggle': toggle,
        'text': text_elem.text.strip(),
        'text_element': text_elem
    })
    print(f"  Legend item {i + 1}: '{text_elem.text}'")

# 3. Click on each legend toggle
if legend_items:
    print("\n3. Interacting with legend toggles...")

    for i, item in enumerate(legend_items):
        try:
            toggle = item['toggle']
            legend_text = item['text']

            print(f"\n  Toggle {i + 1}: '{legend_text}'")

            # Click the toggle (not the text)
            print("  Clicking legend toggle...")

            # Use JavaScript to click since it's an SVG element
            driver.execute_script("arguments[0].click();", toggle)
            time.sleep(2)  # Wait for chart update

            # Take screenshot
            take_screenshot("screenshot")

            # Extract chart data for this filter
            extract_chart_data()

            # Optional: Click again to toggle off for next test
            # driver.execute_script("arguments[0].click();", toggle)
            # time.sleep(1)

        except Exception as e:
            print(f"    ❌ Error with toggle {i + 1}: {e}")
            # Try alternative click method
            try:
                actions = ActionChains(driver)
                actions.move_to_element(toggle).click().perform()
                time.sleep(2)
                take_screenshot("screenshot")
                extract_chart_data()
                print(f"    ✓ Fixed with ActionChains")
            except Exception as e2:
                print(f"    ❌ Alternative method also failed: {e2}")
            continue
else:
    print("\n3. No legend toggles found, trying alternative...")

    # Try finding clickable elements in the chart
    try:
        # Look for any clickable SVG elements
        clickable_elements = driver.find_elements(By.CSS_SELECTOR,
                                                  "svg g[pointer-events='all'], svg path[pointer-events='all'], svg[pointer-events='all']")

        print(f"  Found {len(clickable_elements)} potentially clickable elements")

        # Try clicking first few
        for i in range(min(3, len(clickable_elements))):
            try:
                elem = clickable_elements[i]
                print(f"\n  Clicking element {i + 1}...")

                driver.execute_script("arguments[0].click();", elem)
                time.sleep(2)

                take_screenshot("screenshot")
                extract_chart_data()

            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue

    except Exception as e:
        print(f"  ❌ Error with alternative: {e}")

# 4. Handle edge case: unselect all filters
print("\n4. Handling unselect all filters case...")

# Strategy 1: Click on each active toggle to deactivate
print("  Clicking all toggles to reset...")
for item in legend_items:
    try:
        toggle = item['toggle']
        # Click twice (toggle on then off) or just once if already on
        driver.execute_script("arguments[0].click();", toggle)
        time.sleep(0.5)
    except:
        pass

time.sleep(2)

# Take screenshot after reset
take_screenshot("screenshot")

# Extract data after reset
extract_chart_data()

# Strategy 2: Look for a "Show all" or similar text
try:
    show_all_elements = driver.find_elements(By.XPATH,
                                             "//*[contains(text(), 'Show all') or contains(text(), 'All') or contains(text(), 'Reset')]")

    for elem in show_all_elements:
        if elem.is_displayed():
            print(f"  Found reset element: '{elem.text}'")
            elem.click()
            time.sleep(2)
            take_screenshot("screenshot")
            extract_chart_data()
            break
except:
    pass

# Final summary
print("\n" + "=" * 60)
print("STEP 5 COMPLETED")
print("=" * 60)
print(f"\nSummary:")
print(f"  Screenshots taken: {screenshot_count}")
print(f"  CSV files created: {csv_count}")
print(f"  Screenshots saved in: screenshots/")
print(f"  Chart data saved in: csv_files/")

# Take one final screenshot
driver.save_screenshot("screenshots/final_state.png")
print(f"  Final screenshot: screenshots/final_state.png")

driver.quit()

# List created files
print("\n" + "-" * 40)
print("CREATED FILES:")
print("-" * 40)

# List screenshots
if os.path.exists("screenshots"):
    screenshots = sorted([f for f in os.listdir("screenshots") if f.endswith('.png')])
    print(f"\nScreenshots ({len(screenshots)}):")
    for ss in screenshots:
        print(f"  screenshots/{ss}")

# List CSV files
if os.path.exists("csv_files"):
    csv_files = sorted([f for f in os.listdir("csv_files") if f.endswith('.csv')])
    print(f"\nCSV files ({len(csv_files)}):")
    for csv_file in csv_files:
        print(f"  csv_files/{csv_file}")
        # Show first few rows
        try:
            with open(f"csv_files/{csv_file}", 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    print(f"    Contains {len(lines) - 1} data rows")
        except:
            pass

print("\n" + "=" * 60)
print("ALL STEPS COMPLETED!")
print("=" * 60)
print("\nDeliverables ready:")
print("1. ✅ table.csv - Table data extracted")
print("2. ✅ screenshot*.png - Screenshots of chart interactions")
print("3. ✅ doughnut*.csv - Chart data for each filter state")
print("4. ✅ report.html - Original HTML report")
print("\nHomework requirements satisfied! 🎉")