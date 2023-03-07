import requests

from timekeeper.model import Day


class Hiper:
    url: str = "http://hiper.e-ducativa.x/aj_reloj.cgi"
    accion: str = "validar_guardar_teletrabajo"
    @classmethod
    def register_date(cls, day: Day, legajo: int) -> dict:
        request_data = {
            "accion": cls.accion,
            "dia": day.day_str(),
            "entrada": day.time_in_str(),
            "salida": day.time_out_str(),
            "tele_legajo": legajo,
        }

        response = requests.post(url=cls.url, data=request_data)

        return {"status_code": response.status_code, "text": response.text}
