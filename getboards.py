from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from PIL import Image
from io import BytesIO

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://chess.com/")
driver.maximize_window()
driver.implicitly_wait(10)
login_button = driver.find_element(By.CLASS_NAME, "button.auth.login.ui_v5-button-component.ui_v5-button-primary")
login_button.click()
user_name = driver.find_element(By.ID, "username")
user_name.send_keys(input("Enter your username: "))
password = driver.find_element(By.ID, "password")
password.send_keys(input("Enter your password: "))
log_in = driver.find_element(By.ID, "login")
log_in.click()
settings = driver.find_element(By.CSS_SELECTOR, "span[class = 'icon-font-chess circle-gearwheel'")
settings.click()
board_and_pieces = driver.find_element(By.CSS_SELECTOR, "a[href = 'https://www.chess.com/settings/board']")
board_and_pieces.click()

coordinates = Select(driver.find_element(By.ID, "board_pieces_showCoordinates"))
coordinates.select_by_visible_text("Off")

piece_style = Select(driver.find_element(By.ID, "board_pieces_gamePieceStyle"))
piece_style_list = [option.text for option in piece_style.options]
board_color = Select(driver.find_element(By.ID, "board_pieces_gameBoardColor"))
board_color_list = [option.text for option in board_color.options]


piece_style.select_by_visible_text("Club")
board_color.select_by_visible_text("Brown")

save_button = driver.find_element(By.ID, "board_pieces_save")
save_button.click()
play_button = driver.find_element(By.CSS_SELECTOR, "a[href = 'https://www.chess.com/play']")
play_button.click()

board = driver.find_element(By.ID, "board")

location = board.location
size = board.size

png = driver.get_screenshot_as_png()
img = Image.open(BytesIO(png))

left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']
img = img.crop((left, top, right, bottom))
img.save('screenshot.png')