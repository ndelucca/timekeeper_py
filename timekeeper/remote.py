import logging

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from timekeeper.model import Day


class Hiper:
    url: str = "http://hiper.e-ducativa.x"

    def login(self, username: str, password: str) -> dict:
        login_url = f"{self.url}/login.cgi"
        encoder = MultipartEncoder(
            fields={
                "accion": "",
                "usuario": username,
                "password": password,
            }
        )
        session = requests.Session()

        session.post(
            url=login_url,
            headers={
                "Content-Type": encoder.content_type,
            },
            data=encoder,
            allow_redirects=True,
        )
        session_cookies = session.cookies.get_dict()

        if not session_cookies:
            raise Exception("Can't login.")

        return session.cookies.get_dict()

    def register_date(self, day: Day, cookies: dict) -> dict:
        reloj_url = f"{self.url}/aj_reloj.cgi"
        request_data = {
            "accion": "validar_guardar_teletrabajo",
            "dia": day.day_str(),
            "entrada": day.time_in_str(),
            "salida": day.time_out_str(),
        }

        response = requests.post(url=reloj_url, json=request_data, cookies=cookies)

        if response.status_code == 200 and response.text == '{"estado":1}':
            return True

        logging.warning(response.text)
        return False
