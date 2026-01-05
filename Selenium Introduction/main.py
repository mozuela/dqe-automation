"""
Selenium Homework Automation
Author: Julia Mendoza
Date: 2026-01-05

1. Use Context Manager for Selenium WebDriver
Objective: Create a context manager for initializing and quitting the Selenium WebDriver.

2. Table Interaction
Objective: Extract the content of the table in the HTML report and save it as a CSV file.

3. Doughnut Chart Interaction
Objective: Iterate through filters for the doughnut chart, take screenshots at each stage, and save the chart data into CSV files.
"""

import logging
import time
import csv
import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selenium_homework.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

#Context manager for Selenium WebDriver initialization
class SeleniumWebDriverContextManager:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless

    def __enter__(self):
        try:
            # Simple Chrome options
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")

            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

            logger.info("Initializing Chrome WebDriver...")

            self.driver = webdriver.Chrome(options=chrome_options)

            self.driver.implicitly_wait(10)
            logger.info("WebDriver initialized successfully")
            return self.driver

        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup WebDriver"""
        try:
            if self.driver:
                logger.info("Closing WebDriver...")
                self.driver.quit()
                self.driver = None
                logger.info("WebDriver cleanup complete")
        except Exception as e:
            logger.error(f"Error during WebDriver cleanup: {str(e)}")

        if exc_type is not None:
            logger.warning(f"Exception in context block: {exc_type.__name__}: {exc_value}")

        return False

#Main automation class
class ReportAutomation:


    def __init__(self, html_file_path: str):
        self.html_file_path = html_file_path
        self.driver = None
        self.base_url = f"file://{os.path.abspath(html_file_path)}"

        # Create output directories
        self.create_directories()

        # Counters for file naming
        self.screenshot_count = 0
        self.csv_count = 0

    #Create directories for output files
    def create_directories(self):
        directories = ['screenshots', 'csv_files']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created/verified directory: {directory}")

    #Take and save screenshot with sequential naming
    def take_screenshot(self, prefix="screenshot"):
        filename = f"screenshots/{prefix}{self.screenshot_count}.png"
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        self.screenshot_count += 1
        return filename
    #Extract table data
    def extract_table_data(self):
        logger.info("Starting table data extraction...")

        try:
            # HTML report
            self.driver.get(self.base_url)
            time.sleep(5)  # Wait for page load

            # Find SVG elements that contain the table
            print("\n1. Finding table elements...")

            # Find text elements with class 'cell-text'
            cell_texts = self.driver.find_elements(By.CSS_SELECTOR, "text.cell-text")
            print(f"   Found {len(cell_texts)} cell-text elements")

            if not cell_texts:
                raise NoSuchElementException("No table elements found")

            # Organize data by position
            table_data = {}
            for elem in cell_texts:
                text = elem.text.strip()
                if text:
                    location = elem.location
                    key = f"{location['y']}_{location['x']}"
                    table_data[key] = {
                        'text': text,
                        'x': location['x'],
                        'y': location['y']
                    }

            # Sort by Y position (rows), then X position (columns)
            sorted_items = sorted(table_data.items(), key=lambda x: (x[1]['y'], x[1]['x']))

            # Group by Y position to find rows
            rows = {}
            for key, data in sorted_items:
                y = data['y']
                if y not in rows:
                    rows[y] = []
                rows[y].append(data)

            # Convert to table structure
            table_rows = []
            for y_pos in sorted(rows.keys()):
                row_data = rows[y_pos]
                row_data.sort(key=lambda x: x['x'])
                row_texts = [cell['text'] for cell in row_data]
                table_rows.append(row_texts)

            # Identify headers and data
            headers = ['Facility Type', 'Visit Date', 'Average Time Spent']
            data_rows = []

            for i, row in enumerate(table_rows):
                if 'Facility Type' in ' '.join(row):
                    print(f"   Header row found: {row}")
                    if len(row) >= 3:
                        headers = row[:3]
                elif len(row) >= 3:
                    # This is a data row
                    row_text = ' '.join(row)
                    if any(facility in row_text for facility in ['Clinic', 'Hospital', 'Specialty Center']):
                        data_rows.append(row[:3])

            print(f"   Extracted {len(data_rows)} data rows")

            # Save to CSV
            csv_path = "csv_files/table.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data_rows)

            print(f"\n Table Extraction Complete:")
            print(f"   File: {csv_path}")
            print(f"   Headers: {headers}")
            print(f"   Rows extracted: {len(data_rows)}")
            if data_rows:
                print(f"   Sample (first 3 rows):")
                for i, row in enumerate(data_rows[:3]):
                    print(f"     Row {i+1}: {row}")

            return csv_path

        except Exception as e:
            logger.error(f"Error in table extraction: {e}")
            print(f" Table extraction error: {e}")

            # Create error CSV
            csv_path = "csv_files/table.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Error", "Message"])
                writer.writerow(["Extraction Failed", str(e)])
            return csv_path
    #Extract data from doughnut chart
    def extract_chart_data(self):
        """- Using what worked in Step 5"""
        try:
            chart_data = []

            legend_items = self.driver.find_elements(By.CSS_SELECTOR, "text.legendtext")

            for item in legend_items:
                text = item.text.strip()
                if text:
                    parts = text.split()
                    if len(parts) >= 2:
                        facility = ' '.join(parts[:-1])
                        value = parts[-1]
                        if value.replace('.', '').isdigit():
                            chart_data.append([facility, value])

            # Save to CSV
            csv_filename = f"csv_files/doughnut{self.csv_count}.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Facility Type', 'Min Average Time Spent'])

                if chart_data:
                    for row in chart_data:
                        writer.writerow(row)
                    logger.info(f"Chart data saved: {csv_filename} ({len(chart_data)} rows)")
                else:
                    # Create empty CSV with headers
                    writer.writerow(['No data', ''])
                    logger.info(f"Empty chart data saved: {csv_filename}")

            self.csv_count += 1
            return csv_filename

        except Exception as e:
            logger.error(f"Error extracting chart data: {e}")

            # Create empty CSV
            csv_filename = f"csv_files/doughnut{self.csv_count}.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Facility Type', 'Min Average Time Spent'])
                writer.writerow(['Error', str(e)])

            self.csv_count += 1
            return csv_filename
    #Interact with doughnut chart
    def interact_with_doughnut_chart(self):
        logger.info("Starting doughnut chart interaction...")

        try:
            # 1. Take initial screenshot (unfiltered state)
            print("\n1. Taking initial screenshot (unfiltered state)...")
            self.take_screenshot()
            self.extract_chart_data()

            # 2. Find and interact with legend toggles
            print("\n2. Finding and interacting with chart filters...")

            # Find legend toggles and texts (worked in testing)
            legend_toggles = self.driver.find_elements(By.CSS_SELECTOR, "rect.legendtoggle")
            legend_texts = self.driver.find_elements(By.CSS_SELECTOR, "text.legendtext")

            legend_items = []
            for i in range(min(len(legend_toggles), len(legend_texts))):
                legend_items.append({
                    'toggle': legend_toggles[i],
                    'text': legend_texts[i].text.strip()
                })

            print(f"   Found {len(legend_items)} filter(s): {[item['text'] for item in legend_items]}")

            # Click on each legend toggle
            for i, item in enumerate(legend_items):
                try:
                    print(f"\n   Filter {i+1}: '{item['text']}'")
                    print("   Clicking filter...")

                    # Use ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(item['toggle']).click().perform()
                    time.sleep(2)  # Wait for chart update

                    # Take screenshot
                    self.take_screenshot()

                    # Extract chart data
                    self.extract_chart_data()

                except Exception as e:
                    logger.error(f"Error with filter {i+1}: {e}")
                    print(f"  Error (but continuing): {e}")
                    continue

            # 3. Handle edge case: unselect all filters
            print("\n3. Handling unselect all filters case...")

            # Click all toggles to reset
            for item in legend_items:
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(item['toggle']).click().perform()
                    time.sleep(0.5)
                except:
                    pass

            time.sleep(2)

            # Take screenshot after reset
            self.take_screenshot()

            # Extract data after reset
            self.extract_chart_data()

            print("\n Doughnut chart interaction completed!")

        except Exception as e:
            logger.error(f"Error in doughnut chart interaction: {e}")
            print(f" Error: {e}")

    def run_automation(self):
        """Run complete automation workflow"""
        print("\n" + "="*70)
        print("SELENIUM HOMEWORK AUTOMATION")
        print("="*70)

        # Check if HTML file exists
        if not os.path.exists(self.html_file_path):
            print(f" Error: HTML file '{self.html_file_path}' not found!")
            print("Please copy the HTML report from Podman container to this directory.")
            return

        print(f"📄 HTML Report: {self.html_file_path}")
        print(f"📁 Output directories: screenshots/, csv_files/")
        print("="*70)

        try:
            with SeleniumWebDriverContextManager(headless=False) as driver:
                self.driver = driver

                # Task 1: Extract table data
                print("\nTASK 1: EXTRACTING TABLE DATA")
                print("-"*40)
                self.extract_table_data()

                # Task 2: Interact with doughnut chart
                print("\nTASK 2: INTERACTING WITH DOUGHNUT CHART")
                print("-"*40)
                self.interact_with_doughnut_chart()

        except Exception as e:
            logger.error(f"Automation failed: {e}")
            print(f"\n Automation failed with error: {e}")
            return

        # Generate summary report
        self.generate_summary()

    #Summary
    def generate_summary(self):
        print("\n" + "="*70)
        print("AUTOMATION SUMMARY")
        print("="*70)

        # Count screenshots
        screenshots = []
        if os.path.exists("screenshots"):
            screenshots = sorted([f for f in os.listdir("screenshots") if f.endswith('.png')])

        # Count CSV files
        csv_files = []
        if os.path.exists("csv_files"):
            csv_files = sorted([f for f in os.listdir("csv_files") if f.endswith('.csv')])

        print(f"\n SCREENSHOTS ({len(screenshots)} files):")
        for i, screenshot in enumerate(screenshots):
            print(f"   {i:2d}. screenshots/{screenshot}")

        print(f"\n CSV FILES ({len(csv_files)} files):")
        for i, csv_file in enumerate(csv_files):
            filepath = f"csv_files/{csv_file}"
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    row_count = sum(1 for _ in f) - 1  # Exclude header
                status = "✓" if row_count > 0 else "⚠"
                print(f"   {i:2d}. {csv_file} {status} {row_count} data rows")
            except:
                print(f"   {i:2d}. {csv_file} Error reading")


def main():
    # Configuration
    HTML_FILE = "report.html"

    # Run automation
    automator = ReportAutomation(HTML_FILE)
    automator.run_automation()


if __name__ == "__main__":
    main()