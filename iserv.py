import datetime
import requests
import bs4
from bs4 import *


DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday"
]


class LoginError(Exception):
    pass


class IServ:
    paths = {
        "login": "/iserv/app/login",
        "logout": "/iserv/app/logout",
        "plan": "/iserv/plan/show/raw/"
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
        # TODO check in header
        if IServ.messages["login_failed"] in r.text:
            raise LoginError("Login failed")

        # find and store csrf token, needed on logout
        self._csrf_token = self._find_csrf(r.text)

        # return True if login was successful
        return True

    def logout(self):
        self._s.get(
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

    def plan_changes(
            self,
            courses=None,
            days=None,
            week: int = datetime.date.today().isocalendar()[1],
            plan_name="0_Vertretungen (Schüler)"
    ):
        # default args
        if days is None:
            days = [""]
        if type(days) == str:
            days = [days]
        days = [d.lower() for d in days]

        if courses is None:
            courses = [""]
        if type(courses) == str:
            courses = [courses]
        courses = [c.lower() for c in courses]

        # TODO on sunday next week
        # get doc
        r = self._s.get(
            url=self.domain + self.paths["plan"] + plan_name + "/" + str(week) + "/w/w00000.htm"
        )
        # validate return
        if not r.headers["content-disposition"] == "inline; filename=w00000.htm":
            raise Exception("invalid return")

        # create soup
        s = BeautifulSoup(r.text, "html.parser")  # , from_encoding="utf-8")

        # get list of needed tables in doc
        tables = s.find_all("table", class_="subst")

        entries = {}

        for i in range(len(tables)):
            # get days
            day_temp = DAYS[i]
            # check day
            if day_temp not in days:
                # skip this table
                continue
            entries[day_temp] = []

            # iterate through all rows of table and store data
            for row in tables[i]:
                if type(row) != bs4.element.NavigableString:
                    # get all values of columns
                    clm = [i.string for i in row.find_all("td")]
                    try:
                        add = False
                        for course in courses:
                            add_temp = True
                            for letter in course:
                                if letter not in clm[0].lower():
                                    add_temp = False
                            if add_temp:
                                add = True
                        if add:
                            details = {
                                "courses": clm[0],
                                "hour": clm[1],
                                "subject": clm[2],
                                "teacher": clm[3],
                                "room": clm[4],
                                "comments": clm[5],
                                "org_subject": clm[6],
                                "org_teacher": clm[7],
                                "type": clm[8],
                            }
                            # print(details)
                            entries[day_temp].append(details)
                    except IndexError:
                        pass
        return entries
