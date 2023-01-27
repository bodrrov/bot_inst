import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from auth_data import username, password,hashtag
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


service = Service(executable_path= 'C:\\Users\Bodrov\\Desktop\\chromedriver_win32\\chromedriver.exe')
driver = webdriver.Chrome(service=service)
try:
    #Авторизация
    driver.get("https://www.instagram.com/")
    time.sleep(10)

    text_box = driver.find_element(by = By.NAME, value="username")
    text_box.clear()
    text_box.send_keys(username)
    time.sleep(2)
    text_box = driver.find_element(by =By.NAME, value="password")
    text_box.clear()
    text_box.send_keys(password + Keys.ENTER)
    time.sleep(7)
    savepush = driver.execute_script("document.getElementsByClassName ('_acan _acao _acas _aj1-')[0].click()")
    time.sleep(7)
    onpush = driver.execute_script("document.getElementsByClassName ('_a9-- _a9_1')[0].click()")
    time.sleep(10)
    for url in posts_urls:
                try:
                    browser.get(url)
                    time.sleep(3)
                    like_button = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                    time.sleep(random.randrange(80, 100))
                except Exception as ex:
                    print(ex)