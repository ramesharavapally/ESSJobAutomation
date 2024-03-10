import json
import openpyxl
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from BaseClass import BaseClass
from selenium_logger import SeleniumLogger
from selenium.common.exceptions import TimeoutException , NoSuchElementException
import traceback
from selenium.webdriver.common.keys import Keys
from readexceldata import get_lovs_source_data

class TestESSLovClass(BaseClass):
        
        
    def perform_cancel_action(self):
        try:                    
            try:                
                _wait = WebDriverWait(self.driver, 5)
                element_explicit = _wait.until(EC.presence_of_element_located((By.XPATH, "(//table[.//img[@title='Error']])[1]")))                    
                self.logger.error('Error message is while processing lov :')
                self.logger.error(self.driver.find_element(By.XPATH,"(//table//td[contains(text(), 'Error:')])[1]").text)
                self.logger.error(self.driver.find_element(By.XPATH,"(//tr[.//img[@title='Error']]//span)[1]").text)                    
                self.driver.find_element(By.XPATH,"//button[@title='Cancel']").click()                
            except:                
                self.driver.find_element(By.XPATH,"//button[@title='Cancel']").click()                
        except Exception as e:
            pass
    
    
    def wait_and_click_element(self, locator):
        while True:
            try:
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
                element.click()
                break
            except TimeoutException:
                print(f"Element {locator} not found, retrying...")
                continue

    def wait_and_send_keys(self, locator, keys):
        while True:
            try:
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
                element.send_keys(keys)
                break
            except TimeoutException:
                print(f"Element {locator} not found, retrying...")
                continue
    
    def wait_and_send_keys_and_tab(self, locator, keys):
        while True:
            try:
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
                element.send_keys(keys)
                element.send_keys(Keys.TAB)        
                break
            except TimeoutException:
                print(f"Element {locator} not found, retrying...")
                continue

    @pytest.mark.lovtest
    def test_create_lovs(self):        
        
        self.logger = SeleniumLogger(log_file='..\logs\lovs.log')
        self.login('https://ebdt-dev1.fa.us2.oraclecloud.com' , 'krishnamurthy.Marella', 'Fusion$1234')           
        
        self.navigate_to_setup_and_maintenance()
        self.navigate_to_tasks()
        self.logger.info('Logged in successfully')
        
        self.search_item("Manage Enterprise Scheduler Job Definitions and Job Sets for Financial, Supply Chain Management, and Related Applications")                        
                        
        
        wait = WebDriverWait(self.driver, 50)
        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[text()='Manage List of Values Sources'])[1]")))
        self.driver.find_element(By.XPATH , "(//a[text()='Manage List of Values Sources'])[1]").click()    
        time.sleep(2)     
        
        # Read data from Excel and convert to JSON
        json_data = get_lovs_source_data('..\data\lovs')
        if json_data is None:
            return     
        json_data = json.loads(json_data)
                
        
        for row in json_data:
            try:
                
                self.wait_and_click_element((By.XPATH, "//img[@title='Create']"))
                
                self.logger.info(f'==============Start processing for LOV {row["user_lov_name"]}')
                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//table[.//tr/td/div[text()='Create List of Values Source']]"))) #wait for popup                                
                
                self.wait_and_send_keys_and_tab((By.XPATH, "//a[@title='Search and Select: Application Name']/ancestor::span/input"), row["application_name"])                                                                     
                self.driver.find_element(By.XPATH,"(//label[text()='User List of Values Source Name']/following::td/input[@type='text'])[1]").send_keys(row["user_lov_name"])
                self.driver.find_element(By.XPATH,"//label[text()='Description']/following::input[@type='text'][1]").send_keys(row["description"])                
                lovTypeDropdown = Select(self.driver.find_element(By.XPATH, ".//label[text()='LOVType']/following::select[1]"))
                lovTypeDropdown.select_by_visible_text(row["lov_type"])                                                 
                self.wait_and_send_keys((By.XPATH, "//label[text()='Query']/following::textarea"), row["query"])
                                                
                # Clicking the 'Save and Close' button
                self.driver.find_element(By.XPATH,"//button[@title='Save and Close']").click()
                self.logger.info(f'End processing for LOV {row["user_lov_name"]}')                
                                                
            except TimeoutException as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"TimeoutException occurred: {str(e)}\n{tb_info}")
                time.sleep(2)
                # self.perform_cancel_action()
            except Exception as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"An unexpected error occurred: {str(e)}\n{tb_info}")
                time.sleep(2)
                # self.perform_cancel_action()
        
        self.logger.info('==============Process cmolpleted==========')
        time.sleep(8)
                
