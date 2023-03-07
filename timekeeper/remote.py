import logging
import requests

from timekeeper.model import Day


class Hiper:
    url: str = "http://hiper.e-ducativa.x/aj_reloj.cgi"
    accion: str = "validar_guardar_teletrabajo"

    @classmethod
    def register_date(cls, day: Day, legajo: str, user_log: str) -> dict:
        request_data = {
            "accion": cls.accion,
            "dia": day.day_str(),
            "entrada": day.time_in_str(),
            "salida": day.time_out_str(),
            "tele_legajo": legajo,
        }

        cookies = {"hiper_usr_log": user_log}

        response = requests.post(url=cls.url, json=request_data, cookies=cookies)

        if response.status_code == 200 and response.text == '{"estado":1}':
            return True

        logging.warning(response.text)
        return False
