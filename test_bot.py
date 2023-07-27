#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src import constants as cons
import requests
import os
import datetime

from pathlib import Path
import time
import pyperclip
import argparse

""" I try to make one bot who make Facebook publications from one list of sentences. I can't make also images posts 
because selenium don't allow to drag and drop from different websites and is only one exercise for fun. I will leave
their arguments for the future. Some functions could only work in Spanish Facebook."""
parser = argparse.ArgumentParser()
parser.add_argument("personal_email", help="Provide the personal email for login.")
args = parser.parse_args()

""" Descargar frases desde constant y implementar pyperclyp o una funcion de selenium para las fotos. """
""" Ask for the password to don't save on cache """
password_keys = input(">Provide the login password before starting:")

class FirefoxBrowser:
    def __init__(self):
        self.seleniumdriver = Path("geckodriver").resolve()
        self.service = Service(self.seleniumdriver)
        self.driver = webdriver.Firefox(service=self.service)
                
    def open_web(self):
        """ Open the web and maximize the window. """
        self.driver.implicitly_wait(5)
        self.driver.get(cons.BASE_URL)
        self.driver.maximize_window()

    def click_cookies(self):
        """ Find and delete the cookies."""
        try:
            essential_cookies = self.driver.find_element(By.CSS_SELECTOR,
                                                         "button[data-testid=cookie-policy-manage-dialog-accept-button]")
            essential_cookies.click()
            time.sleep(1)
        except:
            pass

class WritePost(FirefoxBrowser):
    def __init__(self):
        super().__init__()

    def login_mail(self):
        """ Automate the writing of login email."""
        log_email = self.driver.find_element(By.ID, "email")
        log_email.send_keys(f"{args.personal_email}")
        time.sleep(1)

    def login_password(self):
        """ Automate the writing of login_password."""
        password = self.driver.find_element(By.ID, "pass")
        password.send_keys(password_keys)
        time.sleep(1)

    def make_login(self):
        """ Click on login button and finish this step."""
        login = self.driver.find_element(By.NAME, "login")
        login.click()
        time.sleep(1)

    def profile_main(self):
        """ Click in the profile main page to begin always in the same place."""
        main_page = self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='Inicio']")
        main_page.click()
        time.sleep(2)

    def publication_box(self):
        """ Go to publication box and click to start posting."""
        boton_publicar = self.driver.find_element(By.CSS_SELECTOR, "div.x1lkfr7t:nth-child(1) > span:nth-child(1)")
        boton_publicar.click()
        time.sleep(1)

    def set_post_privacity(self):
        """ Check and make that the post is for all people, by default is in private the first time."""
        boton_publico = self.driver.find_element(By.XPATH, "//span[text()= 'Público']")
        boton_publico.click()
        time.sleep(1)
        boton_comenzar = self.driver.find_element(By.XPATH, "//span[text()= 'Listo']")
        boton_comenzar.click()
        time.sleep(1)

    def write_post(self):
        """ Write the post from the list of posts with for loop, otherwise not allowed."""
        escribir = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div[1]")
        time.sleep(2)
        mensaje = cons.MENSAJES[0]
        self.image = cons.MENSAJES[0].split()
        self.image = self.image[0:2]
        for letter in mensaje:
            escribir.send_keys(letter)
            time.sleep(0.1)
        escribir.send_keys(Keys.ENTER)
        for letter in "Egobot 0.1":
            escribir.send_keys(letter)
            time.sleep(0.1)
        time.sleep(1.5)

    def make_post(self):
        """ Click on the botton to publish the post."""
        postear = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='Publicar']")
        postear.click()

    def login_steps(self):
        """ Login steps all in one."""
        self.open_web()
        self.click_cookies()
        self.login_mail()
        self.login_password()
        self.make_login()

    def write_publication_steps(self):
        """ The steps to make post publication"""
        self.login_steps()
        self.profile_main()
        self.publication_box()
        self.set_post_privacity()
        self.write_post()
        self.make_post()

class ImagePost(WritePost):
    def __init__(self):
        super().__init__()
        self.image = cons.MENSAJES[0].split()
        self.image = self.image[0:2]
        self.image_path = ''

    def image_post(self):
        """ Click on the button to upload image."""
        post_image = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='Foto/vídeo']")
        post_image.click()
        time.sleep(1)

    def upload_image(self):
        """ Upload image in publication box """
        upload_image = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div")
        upload_image.click()
        up_image = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]")
        upload_image.send_keys(self.image_path)
        time.sleep(4)

    def abrir_ventana(self):
        """ Open new window with google browser."""
        nueva_ventana = self.driver.get(cons.SEARCH_ENGINE)
        time.sleep(1)

    def download_image(self):
        """ Download the image to a folder"""
        try:
            imagen = self.driver.find_elements(By.TAG_NAME, "img")
            for img in imagen[16:20]:
                if img.get_attribute("src").startswith("https:"):
                    post_image = img.get_attribute("src")
                    break
            request_image = requests.get(post_image)
            new_dir = os.mkdir(os.path.join(os.getcwd(), str(datetime.date.today())))
            os.chdir(str(new_dir))
            with open(f"{post_image}.jpg", "wb") as f:
                for chunk in request_image.iter_content(1024):
                    f.write(chunk)
            self.image_path = os.path.join(new_dir, f"{post_image}.jpg")
            print(self.image_path)
            time.sleep(3)
        except TypeError as e:
            print(f"{e}")
            time.sleep(2)
            #returnar al post o preguntar por si quiere continuar

    def clicar_cookie(self):
        """ Click the cookies, if appear."""
        try:
            cookie = self.driver.find_element(By.CSS_SELECTOR,
                                                     "button[id=W0wltc]")
            time.sleep(1)
            cookie.click()
        except:
            pass

    def search_image(self):
        """ Find image in the search engine."""
        busqueda = self.driver.find_element(By.NAME, "q")
        busqueda.send_keys(self.image, Keys.ENTER)
        time.sleep(4)

    def image_field(self):
        """ Open the images field in the browser """
        image_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/a")
        image_field.click()
        time.sleep(3)

    def nueva_ventana(self):
        """ Open new window."""
        self.driver.execute_script("window.open('');")
        self.driver._switch_to.window(self.driver.window_handles[1])
        self.abrir_ventana()

    def window_change(self):
        """ Change the window """
        self.driver._switch_to.window(self.driver.window_handles[0])

    def image_publication_steps(self):
        self.login_steps()
        self.profile_main()
        self.nueva_ventana()
        self.clicar_cookie()
        self.search_image()
        self.image_field()
        self.download_image()
        self.window_change()
        self.publication_box()
        self.set_post_privacity()
        self.write_post()
        self.image_post()
        self.upload_image()
        self.make_post()



bot = ImagePost()
bot.image_publication_steps()
