import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from data import users_settings_dict
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import os
from selenium.webdriver.chrome.options import  Options
import json
from instapy import InstaPy
from instapy import smart_run

path ="C:\Program Files (x86)\geckodriver.exe"

service = Service(executable_path= 'C:\\Users\Bodrov\\Desktop\\chromedriver_win32\\chromedriver.exe')

class InstagramBot():

    def __init__(self,username, password, window_size):

        self.username = username
        self.password = password
        options = Options()
        options.add_argument(f"--window-size={window_size}")
        #опция скрытия окна
        #options.add_argument("--headless")
        self.browser = webdriver.Chrome(service=service,options = options)

    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    #авторизация
    def login(self):

        browser = self.browser
        browser.get("https://www.instagram.com/")
        time.sleep(random.randrange(4, 6))
        permission_page = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/h2'
        if self.xpath_exists(permission_page):
            browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]").click()
        else:
            print("Разрешения получены автоматически")
        username_input = browser.find_element(by=By.NAME, value="username")
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(random.randrange(3, 5))

        password_input = browser.find_element(by=By.NAME, value="password")
        password_input.clear()
        password_input.send_keys(password + Keys.ENTER)
        time.sleep(5)
        savepush_page = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div'
        push_page = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div'
        if self.xpath_exists(savepush_page):
            browser.execute_script("document.getElementsByClassName ('_acan _acao _acas _aj1-')[0].click()")
        else:
            print("Разрещение на сохранение данных уже получено")
        time.sleep(7)
        if self.xpath_exists(push_page):
             browser.execute_script("document.getElementsByClassName ('_a9-- _a9_1')[0].click()")
        time.sleep(10)

    # просмотр сторис
    def watch_stories(self):
        browser = self.browser
        watching = True
        counter = 0
        limit = random.randint(5, 45)
        browser.execute_script("document.getElementsByClassName ('_aarf x1e56ztr x1gslohp')[0].click()")
        try:
            while watching:
                time.sleep(random.randint(10, 15))
                if random.randint(1, 5) == 5:
                    browser.execute_script("document.getElementsByClassName('_ac0d')[0].click()")
                counter += 1
                if counter > limit:
                    browser.execute_script("document.getElementsByClassName('_abl-')[1].click()")
                    watching = False
        except Exception as E:
            print(E)
            watching = False



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
            like_button.click()
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

            post_count = int(browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/div/span/span").text)
            loops_count = int(post_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация # {i}")
            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + '\n')

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        like_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//button//span//*[name()='svg' and @aria-label='Нравится']")))
                        like_button.click()

                        time.sleep(2)

                        print(f"Лайк на пост: {post_url} успешно поставлен!")
                    except Exception as ex:
                         print(ex)

            self.close_browser()
    # метод подписки на всех подписчиков переданного аккаунта
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


            followers_button = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span")

            followers_count = followers_button.get_attribute("title")
            #followers_count = followers_button.text
            #followers_count = int(followers_count.split(' ')[0])
            a = [k for k in followers_count if k.isdigit()]
            followers_count = (int(''.join(a)))


            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1)[:25]:
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")
                all_urls_div = browser.find_elements(by= By.CLASS_NAME, value = "_aano")
                time.sleep(4)

                for url in all_urls_div:
                    url = url.find_element(by = By.TAG_NAME, value ="a").get_attribute("href")

                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:30]:
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

                            time.sleep(random.randrange(4, 8))

                            if self.xpath_exists("/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div[1]/div/a"):

                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists("/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                if self.xpath_exists(
                                        "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]"):
                                    try:
                                        browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button").click()
                                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists("/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button"):
                                            browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                time.sleep(random.randrange(3, 4))

                        except Exception as ex:
                            print(ex)

            except Exception as ex:
                print(ex)




    #метод для отправки сообщений в директ
    def send_direct_message(self, usernames="", message="", img_path=""):
        browser = self.browser
        time.sleep(random.randrange(3, 5))
        direct_message_button = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div/a/div"
        if not self.xpath_exists(direct_message_button):
            print("Кнопка отправки сообщений не найдена!")
            self.close_browser()
        else:
            print("Отправляем сообщение...")
            direct_message = browser.find_element(by=By.XPATH, value=direct_message_button).click()
            time.sleep(random.randrange(2,4))

        #отключаем всплывающее окно
        if self.xpath_exists("/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div"):
            browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]").click()
        time.sleep(random.randrange(2, 4))

        send_message_button = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div/div[3]/div/button").click()
        time.sleep(random.randrange(4, 8))

        # отправка сообщений нескольким пользователям
        for users in usernames:
        #вводим получателя
            to_input = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input")
            to_input.send_keys(usernames)
            time.sleep(random.randrange(2,4))

            #выбираем получателя из списка
            users_list = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]").find_element_by_tag_name("button").click()
            time.sleep(random.randrange(2, 4))
            next_button = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button/div").click()
            time.sleep(random.randrange(2,4))
        if message:
            text_message_area = browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            text_message_area.send_keys(Keys.ENTER)
            print(f"Сообщение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))
            
        if img_path:
            send_img_input = browser.find_element(by=By.XPATH, value= "html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/button[1]")
            send_img_input.send_keys(img_path)
            print(f"Изображение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

        self.close_browser()
    def unsubscribe_for_all_users(self, userpage):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3,6))

        following_button = browser.find_element(by=By.XPATH, value = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div")
        following_count = following_button.find_element(by=By.TAG_NAME, value = "span").text

        following_count = following_count(filter(lambda x: type(x) is int, following_count))
        following_count= (" ".join(following_count))

        # если количество  подписчиков  больше 999б убираем из числа запятые
        #if ',' in followers_count:
            #following_count = int(''.join(following_count.split(',')))
        #elif '&nbsp' in following_count:
            #following_count = int(''.join(following_count.split('&nbsp')))

        #else:
            #following_count = int(following_count)
        #print(f"Колличество подсписок:{following_count}")

        #time.sleep(random.randrange(2,4))

        loops_count = int(following_count / 10)+ 1
        print(f"Колличество перзагрузок страницы: {loops_count}")

        following_users_dict = {}
        for loop in range(1, loops_count + 1):
            count = 10
            browser.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.randrange(3, 6))

            #вызываем меню подсписок
            following_button = browser.find_element(by=By.XPATH, value = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div")
            following_button.click()
            time.sleep(random.randrange(3, 6))

            #забираем все li из ul, в них хранится кнопка отписки и ссылки на подписки

            following_div_block = browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
            following_users = following_div_block.find_elements(by= By.TAG_NAME, value = "li")
            time.sleep(random.randrange(3, 6))

            for user in following_users:

                if not count:
                    break
                user_url = user.find_element(by= By.TAG_NAME, value = "a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                 #объявляем в словарь пару имя_пользователя: ссылка а аккаунт
                following_users_dict[user_name] = user_url
                following_button= user.find_element(by= By.TAG_NAME, value = "button").click()
                time.sleep(random.randrange(3, 6))
                unfollow_button= browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]")
                print(f"Итерация #{count} >>> Отписался от пользователя {user_name}")
                count -= 1

                time.sleep(random.randrange(120,130 ))
        with open("following_users_dict.txt", "w",encoding= "utf-8") as file:
            json.dump(following_users, file)

        self.close_browser()
    #умная отписка от не подписанных аккаунтов

    def smart_unsubscribe(self, username):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        followers_button = browser.find_element(by= By.XPATH , value = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span")
        followers_count = followers_button.get_text("title")

        following_button = browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span/span")
        following_count = following_button.find_element(by= By.TAG_NAME, value = "span").text

        # если количество  подписчиков  больше 999б убираем из числа запятые
        if ',' in followers_count or following:
            followers_count, following_count = int(''.join(following_count.split(','))), int(''.join(following_count.split(',')))
        else:
            followers_count, following_count = int(following_count), int(following_count)
        print(f"Колличество подсписчиков:{followers_count}")

        followers_loops_count = int(followers_count / 12) + 1
        print(f"Число итераций для сбора подсписчиков: {followers_loops_count}")

        print(f"Колличество подсписчиков:{following_count}")
        following_loops_count = int(following_count / 12) + 1
        print(f"Число итераций для сбора подсписчиков: {following_loops_count}")

        time.sleep(random.randrange(2, 4))

        #собираем список подписчиков
        followers_button.click()
        time.sleep(4)

        followers_ul = browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        try :
            followers_urls = []
            for i in range(1, following_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")
            all_urls_div = followers_ul.find_elements(by= By.TAG_NAME, value = 'li')

            for url in all_urls_div:
                url = url.find_element(by= By.TAG_NAME, value = 'a').get_attribute('href')
                followers_urls.append(url)

            #сохраняем всех подписчиков пользователя в файл
            with open(f"{username}_followers_list.txt", "a") as followers_file:
                for link in followers_urls:
                    followers_file.write(link + "\n")
        except Exception as ex:
            print(ex)
            self.close_browser()


        time.sleep(random.randrange(4, 6))
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        #собираем список подписок

        following_button = browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div")
        following_button.click()
        time.sleep(random.randrange(3, 6))

        following_ul = browser.find_element(by= By.XPATH, value = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")

        try:
            following_uls = []
            print("Запускаем сбор подписок")
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
            time.sleep(random.randrange(2, 4))
            print(f"Итерация #{i}")


            all_urls_div = following_ul.find_element(by=By.TAG_NAME, value='li')

            for url in all_urls_div:
                url = url.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                following_urls.append(url)

            # сохраняем всех подписок пользователя в файл
            with open(f"{username}_following_list.txt", "a") as followers_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            """Сравниваем два списка,если пользователь есть в подписках,но его нет в подсписчиках,заносим его в отдельный список"""

            count = 0
            unfollow_list = []
            for user in following_urls:
                if user not in followers_urls:
                    count +=1
                    unfollow_list.append(user)
            print(f"Нужно отписаться от {count} пользователей")
            #сохраняем всех от кого отписаться в файл

            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(link + "\n")

            print("Запускаем отписку......")
            time.sleep(2)

            #заходим к каждому пользователю на страницу и отписываемся
            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                unfollow_user_list = unfollow_file.readlines()
                unfollow_user_list = [row.strip() for row in unfollow_users_list]

            try:
                 count = len(unfollow_user_list)

                 for user_url in unfollow_list:
                     browser.get(user_url)
                     time.sleep(random.randrange(4, 6))

                     #кнопка отписки
                     unfollow_button = browser.find_element(by = By.XPATH, value = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button")
                     unfollow_button.click()

                     time.sleep(random.randrange(4, 6))
                     #кнопка отписки
                     unfollow_button_confirm = browser.find_element(by = By.XPATH,value = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[7]/div/div/div/div/div/div")
                     unfollow_button_confirm.click()

                     print(f"Отписались от {user_url}")
                     count -= 1
                     print(f"Осталось отписаться от: {count} пользователей")

                     #time.sleep(random.randrange(120,130))
                     time.sleep(random.randrange(4, 6))
            except Exception as ex:
                print(ex)
                self.close_browser()

        except Exception as ex:
            print(ex)
            self.close_browser()

        time.sleep(random.randrange(4, 6))
        self.close_browser()






for user, user_data in users_settings_dict.items():
    username = user_data["login"]
    password = user_data["password"]
    windows_size = user_data["windows_size"]

    #my_bot = InstagramBot(username,password,windows_size)
    #my_bot.login()
    #my_bot.close_browser()
    #time.sleep(random.randrange((6,9)))

my_bot = InstagramBot(username,password,windows_size)
my_bot.login()
#my_bot.watch_stories()
#my_bot.send_direct_message(direct_users_list, "Hello to my little friend!", " /Users/Bodrov/Desktop/bot_inst/python.jpg")
#my_bot.get_all_followers("https://www.instagram.com/daaaria_11/")
#my_bot.unsubscribe_for_all_users(bodrov.a.s)
#my_bot.smart_unsubscribe()




