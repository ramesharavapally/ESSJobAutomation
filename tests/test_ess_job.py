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
from readexceldata import get_jobs_source_data
import configparser

class TestESSJobClass(BaseClass):

    CONFIG_FILE = '..\config.ini'

    def get_connection_details(self ):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config['CONFIG']['ERP_URL'], config['CONFIG']['username'], config['CONFIG']['password']
    
    def wait_until_element_present(self, driver, locator, timeout=10, max_attempts=3):
        """
        Wait until the element identified by the given locator is present in the DOM.

        :param driver: WebDriver instance
        :param locator: tuple (By, locator_value) specifying the locator strategy and value
        :param timeout: Maximum time to wait for the element (default is 10 seconds)
        :param max_attempts: Maximum number of attempts to find the element (default is 3)
        :return: WebElement once it's present
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                wait = WebDriverWait(driver, timeout)
                element = wait.until(EC.presence_of_element_located(locator))
                return element
            except TimeoutException:
                attempts += 1
                print(f"Attempt {attempts}: Element not found. Retrying...")
        raise TimeoutException(f"Element not found after {max_attempts} attempts")

            
    def process_parameter(self, parameter):
        # Fill parameters based on their data types
        param_type = parameter["DataType"]
        try:
            if param_type == "Boolean":            
                self.process_boolean_parameter(parameter=parameter)
            elif param_type == "Date or time":
                self.process_date_parameter(parameter=parameter)
            elif param_type == "Number":
                self.process_number_parameter(parameter=parameter)
            elif param_type == "String":
                self.process_string_parameter(parameter=parameter)
            else:                
                raise ValueError(f"Unsupported parameter data type: {param_type}")        
        except Exception as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"An unexpected error occurred while processing parameter: {str(e)}\n{tb_info}")
                time.sleep(2)
    
    def process_boolean_parameter(self,parameter ):
        wait = WebDriverWait(self.driver, 50)
        self.driver.find_element(By.XPATH, "//label[text()='Parameter Prompt']/following::input[@type='text'][1]").send_keys(parameter['ParameterPrompt'])
        dataTypeDropDown = Select(self.driver.find_element(By.XPATH, "(//label[text()='Data Type']/following::td/select)[1]"))
        dataTypeDropDown.select_by_visible_text(parameter['DataType'])
        time.sleep(2)
        if parameter.get('ReadOnly') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Read only']/preceding-sibling::input[@type='checkbox']")            
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()
            time.sleep(1)
        else:
            if parameter.get('Required') == 'Y':
                checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Required']/preceding-sibling::input[@type='checkbox']")                
                actions = ActionChains(self.driver)
                actions.move_to_element(checkbox_element).click().perform()        
        if parameter.get('DefaultValue') is not None and parameter.get('DefaultValue') != "" :
            defaiultValueDropDown = Select(self.driver.find_element(By.XPATH, "//td[contains(label, 'Default Value')]/following-sibling::td//select"))
            defaiultValueDropDown.select_by_visible_text(parameter['DefaultValue'])
        if parameter.get('Tooltip') is not None and parameter.get('Tooltip') != "":
            self.driver.find_element(By.XPATH, "(//label[text()='Tooltip Text']/following::td/textarea)[1]").send_keys(parameter['Tooltip'])            
        if parameter.get('DontDisplay') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, """//label[text()="Don't display"]/preceding-sibling::input[@type='checkbox']""")
            # Move the mouse to the checkbox element and click on it
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()   
        self.driver.find_element(By.XPATH, "//button[@title='Save and Close']").click()             
        
    
    def process_date_parameter(self , parameter):
        wait = WebDriverWait(self.driver, 50)
        self.driver.find_element(By.XPATH, "//label[text()='Parameter Prompt']/following::input[@type='text'][1]").send_keys(parameter['ParameterPrompt'])
        dataTypeDropDown = Select(self.driver.find_element(By.XPATH, "(//label[text()='Data Type']/following::td/select)[1]"))
        dataTypeDropDown.select_by_visible_text(parameter['DataType'])
        time.sleep(2)
        if parameter.get('ReadOnly') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Read only']/preceding-sibling::input[@type='checkbox']")            
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()
            time.sleep(1)
        else:
            if parameter.get('Required') == 'Y':
                checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Required']/preceding-sibling::input[@type='checkbox']")                
                actions = ActionChains(self.driver)
                actions.move_to_element(checkbox_element).click().perform()        
        if parameter.get('ShowType') == 'Date and time':
            checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Date and time']/preceding::input[@type='radio'][1]")                
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()
        # elif parameter['ShowType'] == 'Date only':
        #     checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Date only']/preceding::input[@type='radio'][1]")                
        #     actions = ActionChains(self.driver)
        #     actions.move_to_element(checkbox_element).click().perform()
        if parameter.get('DefaultDateFormat') is not None and parameter.get('DefaultDateFormat') != "":
            defaultDateFormatDropDown = Select(self.driver.find_element(By.XPATH, "//td[contains(label, 'Default Date Format')]/following-sibling::td//select"))
            defaultDateFormatDropDown.select_by_visible_text(parameter['DefaultDateFormat'])
        if parameter.get('DefaultValue') is not None and parameter.get('DefaultValue') != "":
            defaultValueDropDown = Select(self.driver.find_element(By.XPATH, "//td[contains(label, 'Default Value')]/following-sibling::td//select"))
            defaultValueDropDown.select_by_visible_text(parameter['DefaultValue'])
        if parameter.get('Tooltip') is not None and parameter.get('Tooltip') != "":
            self.driver.find_element(By.XPATH, "(//label[text()='Tooltip Text']/following::td/textarea)[1]").send_keys(parameter['Tooltip'])            
        if parameter.get('DontDisplay') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, """//label[text()="Don't display"]/preceding-sibling::input[@type='checkbox']""")
            # Move the mouse to the checkbox element and click on it
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()       
        self.driver.find_element(By.XPATH, "//button[@title='Save and Close']").click()         
            
        
    def process_number_parameter(self , parameter):
        wait = WebDriverWait(self.driver, 50)
        self.driver.find_element(By.XPATH, "//label[text()='Parameter Prompt']/following::input[@type='text'][1]").send_keys(parameter['ParameterPrompt'])
        dataTypeDropDown = Select(self.driver.find_element(By.XPATH, "(//label[text()='Data Type']/following::td/select)[1]"))
        dataTypeDropDown.select_by_visible_text(parameter['DataType'])
        time.sleep(2)
        if parameter.get('ReadOnly') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Read only']/preceding-sibling::input[@type='checkbox']")            
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()
            time.sleep(1)
        else:
            if parameter.get('Required') == 'Y':
                checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Required']/preceding-sibling::input[@type='checkbox']")                
                actions = ActionChains(self.driver)
                actions.move_to_element(checkbox_element).click().perform()        
        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Number Format']/following::select[1]")))
        if parameter.get('NumberFormat') is not None and parameter.get('NumberFormat') != "" :
            numberFormatDropDown = Select(self.driver.find_element(By.XPATH, "//label[text()='Number Format']/following::select[1]"))
            numberFormatDropDown.select_by_visible_text(parameter['NumberFormat'])
        if parameter.get('DefaultValue') is not None and parameter.get('DefaultValue') != "" :
            self.driver.find_element(By.XPATH, "(//label[text()='Default Value']/following::td/input)[1]").send_keys(parameter['DefaultValue'])                
        if parameter.get('Tooltip') is not None and parameter.get('Tooltip') != "":
            self.driver.find_element(By.XPATH, "(//label[text()='Tooltip Text']/following::td/textarea)[1]").send_keys(parameter['Tooltip'])            
        if parameter.get('DontDisplay') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, """//label[text()="Don't display"]/preceding-sibling::input[@type='checkbox']""")
            # Move the mouse to the checkbox element and click on it
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()                
        self.driver.find_element(By.XPATH, "//button[@title='Save and Close']").click()              
        
        
    
    def process_string_parameter(self , parameter):
        wait = WebDriverWait(self.driver, 50)
        time.sleep(3)
        self.wait_until_element_present(self.driver, (By.XPATH, "//label[text()='Parameter Prompt']/following::input[@type='text'][1]"))
        self.driver.find_element(By.XPATH, "//label[text()='Parameter Prompt']/following::input[@type='text'][1]").send_keys(parameter['ParameterPrompt'])
        dataTypeDropDown = Select(self.driver.find_element(By.XPATH, "(//label[text()='Data Type']/following::td/select)[1]"))        
        dataTypeDropDown.select_by_visible_text(parameter['DataType'])
        time.sleep(3)
        if parameter.get('ReadOnly') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Read only']/preceding-sibling::input[@type='checkbox']")            
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform()
            if parameter.get('value') is None or parameter.get('value') == "":
                self.logger.error('Value filed is mandatory for readonly parameters')
                self.driver.find_element(By.XPATH, "//button[@title='Cancel']").click()                
                return                
            time.sleep(2)
            element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "(//label[contains(text(), 'Value')]/following::td/input)[1]")))            
            self.driver.find_element(By.XPATH, "(//label[contains(text(), 'Value')]/following::td/input)[1]").send_keys(parameter['value'])
        
        else:                        
            element_explicit = self.wait_until_element_present(self.driver, (By.XPATH, "(//label[text()='Page Element']/following::td/select)[1]"))
            pageElementDropDown = Select(self.driver.find_element(By.XPATH, "(//label[text()='Page Element']/following::td/select)[1]"))            
            pageElementDropDown.select_by_visible_text(parameter['PageElement'])
            if parameter.get('PageElement') in ('List of values' , 'Choice list'):
                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='List of Values Source']")))
                listOfValuesSource = self.driver.find_element(By.XPATH, "//label[text()='List of Values Source']/following::input[@type='text'][1]")
                listOfValuesSource.send_keys(parameter['ListOfValueSource'])
                # Perform a tab out action
                listOfValuesSource.send_keys(Keys.TAB)        
                # time.sleep(3)                
                element_explicit = self.wait_until_element_present(self.driver, (By.XPATH, "//label[text()='Attribute']"))
                dataTypeDropDown = Select(self.driver.find_element(By.XPATH, "//label[@title='List of values source column from which a value is returned to the job' and text()='Attribute']/following::td/select"))                
                dataTypeDropDown.select_by_visible_text(parameter['Attribute'])
                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//fieldset[legend[contains(text(), 'Display Attributes Available Attributes')]]/ul/li")))
                time.sleep(2)
                self.driver.find_element(By.XPATH, "//a[@title='Move all items to: Selected Attributes']").click() 
                time.sleep(2)
                
            # default value and required can be entered for any PageElement type
            if parameter.get('DefaultValue') is not None and parameter.get('DefaultValue') != "" :
                self.driver.find_element(By.XPATH, "(//label[text()='Default Value']/following::td/input)[1]").send_keys(parameter['DefaultValue'])               
            if parameter.get('Required') == 'Y':
                checkbox_element = self.driver.find_element(By.XPATH, "//label[text()='Required']/preceding-sibling::input[@type='checkbox']")                
                actions = ActionChains(self.driver)
                actions.move_to_element(checkbox_element).click().perform()        
            
        if parameter.get('DontDisplay') == 'Y':
            checkbox_element = self.driver.find_element(By.XPATH, """//label[text()="Don't display"]/preceding-sibling::input[@type='checkbox']""")            
            actions = ActionChains(self.driver)
            actions.move_to_element(checkbox_element).click().perform() 
            
        if parameter.get('Tooltip') is not None and parameter.get('Tooltip') != "":
            self.driver.find_element(By.XPATH, "(//label[text()='Tooltip Text']/following::td/textarea)[1]").send_keys(parameter['Tooltip'])
        self.driver.find_element(By.XPATH, "//button[@title='Save and Close']").click()
        
        
        
        
        
        
        

    @pytest.mark.jobs
    def test_ess_job(self):  

        # Create a logger instance
        self.logger = SeleniumLogger(log_file='..\logs\jobs.log')
        url , username , password = self.get_connection_details()                  
        self.login(url , username, password)
        # self.login('https://fa-evog-dev1-saasfaprod1.fa.ocs.oraclecloud.com', 'Conversion.User', 'Apps@1234')
        self.navigate_to_setup_and_maintenance()
        self.navigate_to_tasks()
        self.logger.info('Logged in successfully')

        self.search_item("Manage Enterprise Scheduler Job Definitions and Job Sets for Financial, Supply Chain Management, and Related Applications")
        wait = WebDriverWait(self.driver, 50)

        # Create jobs from JSON data using a loop
        json_data = get_jobs_source_data('..\data\jobs')   
        if json_data is None:
            return     
        jobs = json.loads(json_data)    
        
        # self.logger.debug(jobs)    
        
        for job in jobs:
            self.logger.info(f'Start processing of job : {job["display_name"]}')
            try:                
                while True:
                    try:
                        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@title='Create']")))
                        self.driver.find_element(By.XPATH, "//img[@title='Create']").click()                        
                        time.sleep(2)
                        break
                    except Exception:
                        print("Element not found, retrying...")                        
                        continue
                
                # Fill in form details using data from JSON
                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Display Name']/following::input[1]")))
                self.driver.find_element(By.XPATH, "//label[text()='Display Name']/following::input[1]").send_keys(job['display_name'])
                self.driver.find_element(By.XPATH, "//label[text()='Name']/following::input[1]").send_keys(job['name'])
                self.driver.find_element(By.XPATH, "//label[text()='Path']/following::input[1]").send_keys(job['path'])

                applicationDropdown = Select(self.driver.find_element(By.XPATH, "//label[text()='Application']/following::select[1]"))
                applicationDropdown.select_by_visible_text(job['application'])
                
                self.driver.find_element(By.XPATH, "//td[contains(label, 'Description')]/following-sibling::td//textarea").send_keys(job['Description'])
                # self.driver.find_element(By.XPATH, "//td[contains(label, 'Retries')]/following-sibling::td//input").send_keys(job['Retries'])
                # self.driver.find_element(By.XPATH, "//td[contains(label, 'Job Category')]/following-sibling::td//input").send_keys(job['Job_Category'])
                # self.driver.find_element(By.XPATH, "//td[contains(label, 'Timeout Period')]/following-sibling::td//input").send_keys(job['Timeout_Period'])

                jobAppDropDown = Select(self.driver.find_element(By.XPATH, "//label[text()='Job Application Name']/following::select[1]"))
                jobAppDropDown.select_by_visible_text(job['job_application'])

                jobTypeDropDown = Select(self.driver.find_element(By.XPATH, "//label[text()='Job Type']/following::select[1]"))
                jobTypeDropDown.select_by_visible_text(job['job_type'])
                
                defaultOutputFormat = Select(self.driver.find_element(By.XPATH, "//label[text()='Default Output Format']/following::select[1]"))
                defaultOutputFormat.select_by_visible_text(job['Default_Output_Format'])

                self.driver.find_element(By.XPATH, "//label[text()='Report ID']/following::input[1]").send_keys(job['report_id'])

                # Fill parameters if they exist
                if 'parameters' in job:
                    for parameter in job['parameters']:
                        self.logger.info(f'Start processing of Parameter : {parameter["ParameterPrompt"]} and datatype {parameter["DataType"]}')
                        while True:
                            try:    
                                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//a[img[@title='Create']]")))                            
                                self.driver.find_element(By.XPATH, "//a[img[@title='Create']]").click()                        
                                time.sleep(2)
                                break
                            except Exception:
                                print("Element not found, retrying...")                        
                                continue
                        # self.wait_until_element_present(self.driver, (By.XPATH, "//a[img[@title='Create']]"))
                        # self.driver.find_element(By.XPATH, "//a[img[@title='Create']]").click()                        
                        self.wait_until_element_present(self.driver, (By.XPATH, "//table[.//tr/td/div[text()='Create Parameter']]"))
                        element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//table[.//tr/td/div[text()='Create Parameter']]"))) #wait for popup
                        self.process_parameter(parameter)
                        self.logger.info(f'End processing of Parameter : {parameter["ParameterPrompt"]}')

                self.driver.find_element(By.XPATH, "//button[contains(text(),'ave and Close')]").click()

                element_explicit = wait.until(EC.presence_of_element_located((By.XPATH, "//table[tbody/tr[td[contains(text(),'Confirmation')]] and tbody/tr[td[contains(text(),'Your changes were saved.')]]]")))
                confirmation_message = self.driver.find_element(By.XPATH, "//table[.//img[@title='Confirmation']]/tbody/tr[2]/td[2]").text
                print(confirmation_message)
                self.logger.debug(f'confirmation_message {confirmation_message}')
                self.logger.info(f'End processing of job : {job["display_name"]}')
            except TimeoutException as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"TimeoutException occurred: {str(e)}\n{tb_info}")
                time.sleep(2)
            except Exception as e:
                tb_info = traceback.format_exc()
                self.logger.error(f"An unexpected error occurred: {str(e)}\n{tb_info}")
                time.sleep(2)
        
        time.sleep(15)
