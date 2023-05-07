import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from PIL import Image
from io import BytesIO

BASE_URL = "https://chess.com/"
LOGIN_BUTTON = "button.auth.login.ui_v5-button-component.ui_v5-button-primary"
USERNAME_ELEMENT_ID = "username"
PASSWORD_ELEMENT_ID = "password"
USERNAME_ENV_VARIABLE = "CHESS_USERNAME"
PASSWORD_ENV_VARIABLE = "CHESS_PASSWORD"
BOARD_AND_PIECES_TAG = "a[href = 'https://www.chess.com/settings/board']"
LOGIN_ELEMENT_ID_IN_LOGIN_PAGE = "login"
SETTINGS_CSS = "span[class = 'icon-font-chess circle-gearwheel'"
COORDINATES_ELEMENT_ID = "board_pieces_showCoordinates"
PIECE_STYLE_ELEMENT_ID = "board_pieces_gamePieceStyle"
BOARD_COLOR_ELEMENT_ID = "board_pieces_gameBoardColor"
SAVED_IMAGES_PATH = "boardimages"
LAST_SAVED_PIECE_SET_FILE = "last_complete_piece_set.txt"
SAVE_BUTTON_ELEMENT_ID = "board_pieces_save"
PLAY_BUTTON_CSS = "a[href = 'https://www.chess.com/play']"
BOARD_ELEMENT_ID = "board"


def main():
    driver = create_driver()
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    driver.maximize_window()
    login(driver)
    go_to_settings_page(driver)
    go_to_board_and_pieces_settings(driver)
    turn_off_board_coordinate(driver)
    piece_style = select_drop_down_element(driver, PIECE_STYLE_ELEMENT_ID)
    board_color = select_drop_down_element(driver, BOARD_COLOR_ELEMENT_ID)
    piece_style_list = create_options_list(piece_style)
    board_color_list = create_options_list(board_color)

    # To avoid repeating the process for already saved boards where an error interrupts the process
    piece_loop_start_index = set_piece_loop_start_index(LAST_SAVED_PIECE_SET_FILE, piece_style_list)
    # To limit the process to 2-D boards
    piece_loop_end_index = set_piece_loop_end_index(piece_style_list)

    os.makedirs(SAVED_IMAGES_PATH, exist_ok=True)
    save_all_board_images(driver, piece_style_list, board_color_list, piece_loop_start_index, piece_loop_end_index)


def login(driver):

    login_button = driver.find_element(By.CLASS_NAME, LOGIN_BUTTON)
    login_button.click()
    user_name = driver.find_element(By.ID, USERNAME_ELEMENT_ID)
    user_name.send_keys(os.environ[USERNAME_ENV_VARIABLE])
    password = driver.find_element(By.ID, PASSWORD_ELEMENT_ID)
    password.send_keys(os.environ[PASSWORD_ENV_VARIABLE])
    log_in = driver.find_element(By.ID, LOGIN_ELEMENT_ID_IN_LOGIN_PAGE)
    log_in.click()


def go_to_settings_page(driver):
    settings = driver.find_element(By.CSS_SELECTOR, SETTINGS_CSS)
    settings.click()


def go_to_board_and_pieces_settings(driver):
    board_and_pieces = driver.find_element(By.CSS_SELECTOR, BOARD_AND_PIECES_TAG)
    board_and_pieces.click()


def turn_off_board_coordinate(driver):
    coordinates = Select(driver.find_element(By.ID, COORDINATES_ELEMENT_ID))
    coordinates.select_by_visible_text("Off")


def select_drop_down_element(driver, element_id):
    return Select(driver.find_element(By.ID, element_id))


def click_save_settings(driver):
    save_button = driver.find_element(By.ID, SAVE_BUTTON_ELEMENT_ID)
    save_button.click()


def click_play_button(driver):
    play_button = driver.find_element(By.CSS_SELECTOR, PLAY_BUTTON_CSS)
    play_button.click()


def crop_image(screenshot_png, element):
    location = element.location
    size = element.size
    img = Image.open(BytesIO(screenshot_png))
    left = location["x"]
    top = location["y"]
    right = location["x"] + size["width"]
    bottom = location["y"] + size["height"]
    return img.crop((left, top, right, bottom))


def save_image(img, piece_set_name, board_name):
    img.save(
        f"{SAVED_IMAGES_PATH}/{piece_set_name.replace(' ', '')}{board_name.replace(' ', '')}.png")


def save_all_board_images(driver, piece_style_list, board_color_list, piece_loop_start_index, piece_loop_end_index):
    for piece_style_name in piece_style_list[piece_loop_start_index:piece_loop_end_index]:
        for board_color_name in board_color_list:
            piece_style = select_drop_down_element(driver, PIECE_STYLE_ELEMENT_ID)
            board_color = select_drop_down_element(driver, BOARD_COLOR_ELEMENT_ID)
            piece_style.select_by_visible_text(piece_style_name)
            board_color.select_by_visible_text(board_color_name)
            click_save_settings(driver)
            click_play_button(driver)
            screenshot_png = driver.get_screenshot_as_png()
            board = driver.find_element(By.ID, BOARD_ELEMENT_ID)
            cropped_image = crop_image(screenshot_png, board)
            save_image(cropped_image, piece_style_name, board_color_name)
            go_to_settings_page(driver)
            go_to_board_and_pieces_settings(driver)

        with open(LAST_SAVED_PIECE_SET_FILE, "w") as f:
            f.write(piece_style_name)


def create_driver():
    options = Options()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_options_list(dropdown_element):
    return [option.text for option in dropdown_element.options]


def set_piece_loop_start_index(saved_piece_file, piece_style_list):
    if os.path.exists(saved_piece_file):
        with open(saved_piece_file, "r") as f:
            last_saved_piece_set = f.read()
        start_index = piece_style_list.index(last_saved_piece_set) + 1
    else:
        start_index = 0
    return start_index


def set_piece_loop_end_index(piece_style_list):
    return [idx for idx, style in enumerate(piece_style_list) if '3D' in style][0]


if __name__ == '__main__':
    main()
