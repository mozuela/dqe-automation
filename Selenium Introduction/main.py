"""
Selenium HOMEWORK
Julia Mendoza Verduzco

Use Context Manager for Selenium WebDriver
    Objective: Create a context manager for initializing and quitting the Selenium WebDriver.
    Steps:
        Write a class-based context manager inside the main script.
        Use this context manager to ensure proper setup and teardown of the Selenium WebDriver.
Table Interaction
    Objective: Extract the content of the table in the HTML report and save it as a CSV file.
    Steps:
        Locate the table in the HTML report using Selenium.
        Read the content (rows and columns) of the table.
        Save the table content into a CSV file named table.csv.
Doughnut Chart Interaction
    Objective: Iterate through filters for the doughnut chart, take screenshots at each stage, and save the chart data into CSV files.
    Steps:
        Take a screenshot of the doughnut chart in its initial (unfiltered) state.
        Iterate through each filter option on the doughnut chart:
        Click on a new filter option.
        Take a screenshot after applying the filter.
        Extract the data of the doughnut chart for the current filter and save it in a CSV file.
        Handle the edge case where all filters are unselected (if applicable).

"""
import logging
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Setup logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selenium_homework.log', encoding='utf-8'),
        logging.StreamHandler() #To console
    ]
)

logger = logging.getLogger(__name__)

class SeleniumWebDriverContextManager:
    """
        Context manager for Selenium WebDriver initialization: setup and cleanup of WebDriver
        """
    def __init__(self):
        self.driver = None

    def __enter__(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        logger.info("WebDriver initialized")
        return self.driver

    #Exit and cleanup
    def __exit__(self, exc_type, exc_value, traceback):
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

        return False #To propagate exceptions

class TableExtractor:
    """To extract table data from HTML report"""
    def __init__(self,driver):
        self.driver = driver

    def extract_and_save_csv(self, filename="table.csv"):
        """Extract the content of the table in the HTML report and save it as a CSV file.
    Steps:
        Locate the table in the HTML report using Selenium.
        Read the content (rows and columns) of the table.
        Save the table content into a CSV file named table.csv."""
        print("\n === STEP 2: TABLE EXTRACTION ===")
        try:
            time.sleep(2)
            table = self._find_table_with_locators()

            if not table:
                raise NoSuchElementException("Table not found")

            #Read the content
            headers = self._extract_headers(table)
            rows = self._extract_rows(table)

            print(f"Headers: {headers}")
            print(f"Rows found: {len(rows)}")

            #Save to CSV file_ table.csv
            self._save_to_csv(headers, rows, output_file)
            print(f"Saved to {output_file}")

            return True

        except Exception as e:
            print(f"Error: {str(e)}")
            self._create_error_csv(output_file, str(e))
            return False

    def _find_table_with_locators(self):
        table = None

        # Locator 1: By ID
        print("1. Searching by ID...")
        try:
            table = self.driver.find_element(By.ID, "data-table")
            print("Found by ID")
            return table
        except NoSuchElementException:
            print("Not found by ID")

        # Locator 2: By XPATH
        print("2. Searching by XPATH...")
        try:
            table = self.driver.find_element(By.XPATH, "//table")
            print("Found by XPATH")
            return table
        except NoSuchElementException:
            print("Not found by XPATH")

        # Locator 3: By CSS Selector
        print("3. Searching by CSS Selector...")
        try:
            table = self.driver.find_element(By.CSS_SELECTOR, "table")
            print("Found by CSS Selector")
            return table
        except NoSuchElementException:
        print("Not found by CSS Selector")

        return None

def extract_headers(self, table):



if __name__ == "__main__":
    with SeleniumWebDriverContextManager() as driver:
        # file_path = ...
        # drivet.get(...)
        # ...
