# -*- coding: utf-8 -*-

from selenium import webdriver
from fixture.session import SessionHelper



class Application:

    def __init__(self, browser, base_url):
        if browser == "Chrome":
            self.wd = webdriver.Chrome()
        elif browser == "Firefox":
            self.wd = webdriver.Firefox()
        elif browser == "Edge":
            self.wd = webdriver.Edge()
        else:
            raise ValueError("Nierozpoznana przeglądarka %s" % browser)
        #self.wd.implicitly_wait(1)
        self.session = SessionHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def otwarcie_strony_glownej(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
