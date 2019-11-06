# -*- coding: utf-8 -*-

import pytest
import json
import os.path
# import importlib
# import jsonpickle
from fixture.application import Application
# from fixture.db import DbFixture

# scope = "session"  - jedno uruchomienie przegladarki i następnie uruchomienie testów.
# Bez tego - każdy test = otwarcie przegladarki co wydłuża czas.
# @pytest.fixture(scope = "session")

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        # with - dzięki zastosowaniu tej formy nie musimy zamykać pliku. Automatycznie jest zamykany po przejściu całej metody/funkcji
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
# Fixtura dla wszystkich testów. Dzięki temu nie musimy umieszczać oddzielnej fixtury w każdym tescie./
def app(request):
    # wskazujemy że planujemy wykorzystywać fixture i target
    global fixture
    # możliwość wyboru przeglarkiw  której uruchamia się testy, wpisania hasła i loginu oraz adresu bezpośrednio z konsoli
    browser = request.config.getoption("--browser")
    # jako parametr przenoszona jest wartosć opcji "--target", bierzemy blok 'web' z ładowanej konfiguracji
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])
    # fixture.session.czy_trzeba_sie_zalogowac(login=web_config["login"], haslo=web_config["haslo"])
    return fixture


# @pytest.fixture(scope="session")
# def db(request):
#     db_config = load_config(request.config.getoption("--target"))['db']
#     dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config['password'])
#     def fin():
#         dbfixture.destroy()
#     request.addfinalizer(fin)
#     return dbfixture

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.czy_trzeba_sie_wylogowac()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


# @pytest.fixture
# def check_ui(request):
#     return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="Chrome")
    parser.addoption("--target", action="store", default="target.json")
    # parser.addoption("--check_ui", action="store_true")
    # parser.addoption("--login", action="store", default="admin")
    # parser.addoption("--haslo", action="store", default="secret")


# Ladowanie i konfiguracja danych testowych
# def pytest_generate_tests(metafunc):
#     for fixture in metafunc.fixturenames:
#         if fixture.startswith("data_"):
#             stale_dane_testowe = load_from_module(fixture[5:])
#             metafunc.parametrize(fixture, stale_dane_testowe, ids=[str(x) for x in stale_dane_testowe])
#         elif fixture.startswith("json_"):
#             losowe_dane_testowe = load_from_json(fixture[5:])
#             metafunc.parametrize(fixture, losowe_dane_testowe, ids=[str(x) for x in losowe_dane_testowe])
#
#
# def load_from_module(module):
#     return importlib.import_module("data.%s" % module).stale_dane_testowe
#
#
# def load_from_json(file):
#     # wskazanie lokalizacji pliku, __file__ wskazuje miejsce pliku config, nastepnie wskazanie lokalizacji pliku w średnikach "")
#     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
#         return jsonpickle.decode((f.read()))
