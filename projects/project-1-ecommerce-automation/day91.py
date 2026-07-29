from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Start Chrome browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10) # Wait up to 10 seconds for elements

driver.maximize_window() # Open Chrome in a large window



