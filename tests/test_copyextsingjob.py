import time
import pytest
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from BaseClass import BaseClass
from selenium_logger import SeleniumLogger
from selenium.common.exceptions import TimeoutException
import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from readexceldata import get_standard_jobs_source_data
import configparser
import datetime

class TestStandardESSJobClass(BaseClass):

    CONFIG_FILE = '..\config.ini'

    def get_connection_details(self ):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config['CONFIG']['ERP_URL'], config['CONFIG']['username'], config['CONFIG']['password']
    
            
    @pytest.mark.stjobs
    def test_standard_ess_job(self):  

        # Create a logger instance
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logger = SeleniumLogger(log_file=f'..\logs\standard_jobs_{timestamp}.log')
        url , username , password = self.get_connection_details()                  
        self.login(url , username, password)
        self.navigate_to_setup_and_maintenance()
        self.navigate_to_tasks()
        self.logger.info('Logged in successfully')

        self.search_item("Manage Enterprise Scheduler Job Definitions and Job Sets for Financial, Supply Chain Management, and Related Applications")
        wait = WebDriverWait(self.driver, 50)
        
        time.sleep(5)
        
        # Create jobs from JSON data using a loop
        json_data = get_standard_jobs_source_data('..\data\standardjobs')
        if json_data is None:
            return     
        jobs = json.loads(json_data)    
        for job in jobs:            
            try:
                self.logger.info(f"Start processing of job : {job['standard_job_name']} and custom job {job['custom_job_name']}")
                search_element = self.driver.find_element(By.XPATH, "(//table[@summary='This table contains column headers corresponding to the data body table below']/tbody/tr[following-sibling::tr//div/span[text()='Name']]//input)[2]")
                search_element.clear()
                search_element.send_keys(job['standard_job_name'])
                search_element.send_keys(Keys.ENTER)     
                job_xpath = f"(//table[@summary='Manage Job Definitions']/tbody/tr//span[contains(text(),'{job['standard_job_name']}')])[1]"                                                               
                self.driver.find_element(By.XPATH, job_xpath).click()
                self.driver.find_element(By.XPATH , "//img[@title='Duplicate']").click()
                time.sleep(2)
                self.driver.find_element(By.XPATH , "//img[@title='Edit']").click()
                time.sleep(5)
                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Display Name']/following::input[1]")))
                element_explicit.clear()
                self.driver.find_element(By.XPATH, "//label[text()='Display Name']/following::input[1]").send_keys(job['custom_job_name'])
                self.driver.find_element(By.XPATH, "//label[text()='Name']/following::input[1]").send_keys(job['custom_job_id'])
                self.driver.find_element(By.XPATH, "//label[text()='Path']/following::input[1]").send_keys(job['job_path'])
                

                self.driver.find_element(By.XPATH, "//label[text()='Report ID']/following::input[1]").send_keys(job['report_id'])
                
                self.driver.find_element(By.XPATH, "//button[contains(text(),'ave and Close')]").click()
                
                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//table[tbody/tr[td[contains(text(),'Confirmation')]] and tbody/tr[td[contains(text(),'Your changes were saved.')]]]")))
                confirmation_message = self.driver.find_element(By.XPATH, "//table[.//img[@title='Confirmation']]/tbody/tr[2]/td[2]").text            
                self.logger.debug(f'confirmation_message {confirmation_message}')                
                self.logger.info(f"End processing of job : {job['standard_job_name']} and custom job {job['custom_job_name']}")
            except TimeoutException as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"TimeoutException occurred: {str(e)}\n{tb_info}")
                time.sleep(2)
            except Exception as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"An unexpected error occurred: {str(e)}\n{tb_info}")
                time.sleep(2)
        
        
        
        
        time.sleep(15)
