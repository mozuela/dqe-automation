from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


def test_html_structure():
    html_file = "index.html"
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found!")
        return

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        url = f"file://{os.path.abspath(html_file)}"
        driver.get(url)

        print("Page Title:", driver.title)
        print("\nFinding tables...")
        tables = driver.find_elements("tag name", "table")
        print(f"Found {len(tables)} table(s)")

        for i, table in enumerate(tables):
            print(f"\nTable {i + 1}:")
            print(f"  ID: {table.get_attribute('id')}")
            print(f"  Class: {table.get_attribute('class')}")
            rows = table.find_elements("tag name", "tr")
            print(f"  Rows: {len(rows)}")

            if rows:
                headers = rows[0].find_elements("tag name", "th")
                if headers:
                    print(f"  Headers: {[h.text for h in headers]}")

        print("\nFinding charts...")
        chart_selectors = ["canvas", "svg", "[class*='chart']", "[id*='chart']"]
        for selector in chart_selectors:
            elements = driver.find_elements("css selector", selector)
            if elements:
                print(f"  Found {len(elements)} element(s) with selector: {selector}")

        print("\nFinding filter elements...")
        filter_selectors = ["button", "[class*='filter']", "[id*='filter']", "input[type='checkbox']"]
        for selector in filter_selectors:
            elements = driver.find_elements("css selector", selector)
            if elements:
                print(f"  Found {len(elements)} element(s) with selector: {selector}")
                for elem in elements[:3]:  # Show first 3
                    print(
                        f"    - Text: '{elem.text[:50]}' | ID: {elem.get_attribute('id')} | Class: {elem.get_attribute('class')}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_html_structure()