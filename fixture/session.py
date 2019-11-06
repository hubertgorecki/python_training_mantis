# -*- coding: utf-8 -*-


class SessionHelper:
    def __init__(self, app):
        self.app = app

    def zalogowanie(self, login, haslo):
        wd = self.app.wd
        self.app.otwarcie_strony_glownej()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(login)
        wd.find_element_by_xpath("//input[@value='Zaloguj się']").click()
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(haslo)
        wd.find_element_by_xpath("//input[@value='Zaloguj się']").click()

    def wylogowanie(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Wyloguj").click()

    def czy_trzeba_sie_wylogowac(self):
        wd = self.app.wd
        if self.czy_zalogowany():
            self.wylogowanie()

    def czy_zalogowany(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Wyloguj")) > 0

    def czy_zalogowany_jako(self, login):
        wd = self.app.wd
        return self.zwraca_login_zalogowanego == login

    def zwraca_login_zalogowanego(self):
        wd = self.app.wd
        return wd.find_element_by_xpath("//li//a//span[@class='user-info']").text

    def czy_trzeba_sie_zalogowac(self, login, haslo):
        wd = self.app.wd
        if self.czy_zalogowany():
            if self.czy_zalogowany_jako(login):
                return
            else:
                self.wylogowanie()
        self.zalogowanie(login, haslo)
