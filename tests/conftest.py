import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="class")
def setup(request):
    
    # Set the desired zoom level (e.g., 80%)
    zoom_level = 0.8

    # Create ChromeOptions and add the device scale factor option
    chrome_options = Options()
    chrome_options.add_argument(f"--force-device-scale-factor={zoom_level}")

    service_obj = Service('../chromedriver.exe')
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)    
    driver.maximize_window()
    driver.implicitly_wait(5)
    request.cls.driver = driver
    yield
    driver.quit()

