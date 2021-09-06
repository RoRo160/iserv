import requests
from bs4 import *


class LoginError(Exception):
    pass


class IServ:
    paths = {
        "login": "/iserv/app/login",
        "logout": "/iserv/app/logout"
    }
    messages = {
        "login_failed": "Anmeldung fehlgeschlagen!"
    }

    def __init__(self, domain):
        self.domain = domain
        self._csrf_token = None
        self._s = requests.Session()

    def login(self, user, pw):
        # send post request with session object
        r = self._s.post(
            url=self.domain + IServ.paths['login'],         # login path
            data=f"_password={pw}&_username={user}",        # pw ad user in body of request
            headers={
                "Content-Type": "application/x-www-form-urlencoded"     # tell server kind of form, necessary
            }
        )

        # check if login was successful
        if IServ.messages["login_failed"] in r.text:
            raise LoginError("Login failed")

        # find and store csrf token, needed on logout
        self._csrf_token = self._find_csrf(r.text)

        # return True if login was successful
        return True

    def logout(self):
        r = self._s.get(
            # login path
            url=self.domain + IServ.paths['logout'],
            # add csrf token to query
            params={"_csrf": self._csrf_token}
        )

    @staticmethod
    def _find_csrf(doc: str):
        s = BeautifulSoup(doc, "html.parser")
        tag = s.find('body')\
            .find_all('div')[0]\
            .find_all('div')[0]\
            .find_all('ul')[0]\
            .find_all('li')[1]\
            .find('div')\
            .find('ul')\
            .find_all('li')[4]\
            .find('a')

        return tag.attrs["href"].split('=')[-1]
