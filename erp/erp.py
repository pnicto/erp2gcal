# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver = webdriver.Edge()

# Login logic
driver.get("https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?NavColl=true&ICAGTarget=start")

WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'PATRANSACTIONTITLE')))

schedule = driver.execute_script("return document.querySelector('.PSLEVEL1GRIDWBO')")

rawTableData = schedule.text

