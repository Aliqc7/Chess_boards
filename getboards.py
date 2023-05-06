from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://chess.com/")
driver.maximize_window()
login_button = driver.find_element(By.CLASS_NAME, "button.auth.login.ui_v5-button-component.ui_v5-button-primary")
login_button.click()
user_name = driver.find_element(By.ID, "username")
user_name.send_keys(input("Enter your Username"))
password = driver.find_element(By.ID, "password")
password.send_keys(input("Enter your Password"))
log_in = driver.find_element(By.ID, "login")
log_in.click()