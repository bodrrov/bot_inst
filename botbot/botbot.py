import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from auth_data import username, password,hashtag
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import os

service = Service(executable_path= 'C:\\Users\Bodrov\\Desktop\\chromedriver_win32\\chromedriver.exe')
class InstagramBot():

    def __init__(self,username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(service=service)

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    def login(self):

        browser = self.browser
        browser.get("https://www.instagram.com/")
        time.sleep(random.randrange(8, 10))

        username_input = browser.find_element(by=By.NAME, value="username")
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(random.randrange(3, 5))

        password_input = browser.find_element(by=By.NAME, value="password")
        password_input.clear()
        password_input.send_keys(password + Keys.ENTER)
        time.sleep(10)

    def like_photo_by_hashtag(self, hashtag):

        browser = self.browser
        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}")
        time.sleep(10)
        links = browser.find_elements(by=By.TAG_NAME, value="a")

        post_urls = []
        for item in links:
            link = item.get_attribute("href")

            # Фильтруем ссылки
            if "/p/" in link:
                post_urls.append(link)
                print(link)
            print(link)

        # Ставим лайки
        for url in post_urls:
            try:
                browser.get(url)
                time.sleep(10)
                like_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")))
                like_button.click()
                time.sleep(random.randrange(20, 30))
            except Exception as ex:
                print(ex)
                self.close_browser()

    #проверяем по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exists = True
        except  NoSuchElementException:
            exists = False
        return exists

    #ставим лайк на пост по прямой ссылке
    def put_exactly_like(self,userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)
        wrong_userpage = '//*[@id="mount_0_0_lR"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")))
            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    def put_many_likes(self,userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        wrong_userpage = '//*[@id="mount_0_0_lR"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            like_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")))
            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    def get_all_followers(self,userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

         #создаем папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаем папку пользователя {file_name}.")
            os.mkdir(file_name)
        wrong_userpage = '//*[@id="mount_0_0_lR"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно найден, ставим лайки!")
            time.sleep(2)

            like_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")))
            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

            followers_button = browser.find_element_by_xpath(
                "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div")
            followers_count = followers_button.text
            followers_count = int(followers_count.split(' ')[0])
            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:10]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                # print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/a"):

                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists(
                                    "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exists(
                                        "/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_xpath(
                                            "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]").click()
                                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists(
                                                "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button"):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(7, 15))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

            self.close_browser()


my_bot = InstagramBot(username,password)
my_bot.login()
my_bot.put_exactly_like("https://www.instagram.com/p/CbKdp6XtMSB/?next=https%3A%2F%2Fwww.instagram.com%2Faccounts%2Fonetap%2F%3Fnext%3D%2F")




