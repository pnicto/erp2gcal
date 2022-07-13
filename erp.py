# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver = webdriver.Edge()

# Function which goes to login page
def navigation_and_login():
    # Goes to this specific url which is the Student Center Section of ERP
    driver.get("https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?NavColl=true&ICAGTarget=start")

    WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'PATRANSACTIONTITLE')))

# Function which returns the registered courses data from ERP
def get_schedule():
    schedule = driver.execute_script("return document.querySelector('.PSLEVEL1GRIDWBO')")
    rawTableData = schedule.text
    # Removes the 2 unecessary items after splitting and returns it as a list
    return rawTableData.split("\n")[2:]


