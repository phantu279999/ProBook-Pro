from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def custom_chrome():
    options_chrome = Options()
    options_chrome.page_load_strategy = "eager"
    options_chrome.add_argument("--start-maximized")
    options_chrome.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options_chrome, service=Service(ChromeDriverManager().install()))

    driver.implicitly_wait(30)

    return driver


def custome_chrome_headless():
    options_chrome = Options()
    options_chrome.page_load_strategy = "eager"
    options_chrome.add_argument("--start-maximized")
    options_chrome.add_argument("--headless")
    options_chrome.add_argument('--ignore-certificate-errors')
    options_chrome.add_argument('--ignore-ssl-errors')
    options_chrome.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options_chrome, service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(30)

    return driver