import logging

import requests

from timekeeper.model import Day


class Hiper:
    url: str = "http://hiper.e-ducativa.x"
    session: str = None

    def login(self, username: str, password: str):
        login_url = f"{self.url}/login.cgi"
        request_data = {
            "accion": "",
            "usuario": username,
            "password": password,
        }

        response = requests.post(
            url=login_url,
            headers={"Content-type": "multipart/form-data"},
            data=request_data,
        )

        self.session = response.cookies

    def register_date(self, day: Day, legajo: str, user_log: str) -> dict:
        reloj_url = f"{self.url}/aj_reloj.cgi"
        request_data = {
            "accion": "validar_guardar_teletrabajo",
            "dia": day.day_str(),
            "entrada": day.time_in_str(),
            "salida": day.time_out_str(),
            "tele_legajo": legajo,
        }

        cookies = {"hiper_usr_log": user_log}

        response = requests.post(url=reloj_url, json=request_data, cookies=cookies)

        if response.status_code == 200 and response.text == '{"estado":1}':
            return True

        logging.warning(response.text)
        return False
