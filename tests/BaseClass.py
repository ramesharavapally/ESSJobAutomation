import pytest
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.mark.usefixtures("setup")
class BaseClass:
            
    def login(self, url ,username, password):
        self.driver.get(url)
        self.driver.find_element(By.CSS_SELECTOR, "#userid").send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@id='btnActive']").click()

    def navigate_to_setup_and_maintenance(self):
        self.driver.find_element(By.XPATH, "//img[@title='Settings and Actions']").click()
        self.driver.find_element(By.XPATH, "//a[text()='Setup and Maintenance']").click()

    def navigate_to_tasks(self):
        self.driver.find_element(By.XPATH, "//div[@title='Tasks']/a/img[@title='Tasks']").click()
        time.sleep(2)
        
    def search_item(self, item_name):
        wait = WebDriverWait(self.driver, 50)
        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Search']")))
        self.driver.find_element(By.XPATH, "//a[text()='Search']").click()
        
        time.sleep(3)

        # Enter search criteria
        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@title='Search']/ancestor::tr//input")))
        self.driver.find_element(By.XPATH, "//img[@title='Search']/ancestor::tr//input").send_keys(item_name)

        # Perform search
        self.driver.find_element(By.XPATH, "//img[@title='Search']").click()

        # Click on the search result
        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[text()='{item_name}']")))
        self.driver.find_element(By.XPATH, f"//a[text()='{item_name}']").click()