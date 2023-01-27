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

    try:
        #Извлекаем сслки из поста
        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}")
        time.sleep(10)
        links = driver.find_elements(by = By.TAG_NAME,value = "a")

        post_urls = []
        for item in links:
            link = item.get_attribute("href")

            #Фильтруем ссылки
            if "/p/" in link:
                post_urls.append(link)
                print(link)
            print(link)

        #Ставим лайки
        for url in post_urls:
            try:
                driver.get(url)
                time.sleep(10)
                like_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")))
                like_button.click()
                time.sleep(random.randrange(20,30))
            except Exception as ex:
                print(ex)
    except Exception as ex:
        print(ex)

except Exception as ex:
    print(ex)