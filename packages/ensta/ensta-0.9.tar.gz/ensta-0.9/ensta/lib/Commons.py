import string
import requests
import requests.cookies
import random
from .Exceptions import NetworkError


class Commons:

    def __init__(self, other):
        self.other = other

    def update_app_id(self):
        app_id_occurrence_string = "\"APP_ID\":\""
        app_id_first_occurrence = self.other.homepage_source.index(app_id_occurrence_string)
        app_id_raw_text = self.other.homepage_source[
                          app_id_first_occurrence + len(app_id_occurrence_string): app_id_first_occurrence + 30]
        self.other.insta_app_id = app_id_raw_text[: app_id_raw_text.index("\"")]

    def refresh_csrf_token(self):
        self.other.csrf_token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        cookie_object = requests.cookies.create_cookie(domain="instagram.com", name="csrftoken", value=self.other.csrf_token)
        self.other.request_session.cookies.set_cookie(cookie_object)

    def update_session(self):
        self.other.request_session = requests.Session()

    def update_homepage_source(self):
        temp_homepage_source = requests.get("https://www.instagram.com").text.strip()

        if temp_homepage_source != "":
            self.other.homepage_source = temp_homepage_source
        else:
            raise NetworkError("Couldn't load instagram homepage.")
