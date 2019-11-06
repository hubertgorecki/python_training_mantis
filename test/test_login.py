from fixture.session import SessionHelper

def test_login(app):
    app.session.zalogowanie("administrator", "root")
    assert app.session.zwraca_login_zalogowanego() == "administrator"