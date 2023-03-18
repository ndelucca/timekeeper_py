"""Configuration module"""
import os
from configparser import ConfigParser
from dataclasses import dataclass, field

from click import ClickException

from timekeeper.model import Times

CONFIG_TEMPLATE = """
[hiper]
legajo = 00
user = USERNAME
"""


class ConfigError(ClickException):
    """Timekeeper configuration exception"""


@dataclass
class Config:
    """Timekeeper Configuration object"""

    model: Times = field(init=False)
    hiper: dict = field(init=False)

    def __post_init__(self):
        home = os.path.expanduser("~")

        database = os.path.join(home, "timekeeper.db")
        self.model = Times(database)

        configuration = os.path.join(home, "timekeeper.conf")
        if not os.path.exists(configuration):
            raise ConfigError(
                (
                    f"{configuration} configuration file missing\n"
                    f"You could create one using this structure\n{CONFIG_TEMPLATE}"
                )
            )
        conf = ConfigParser()
        conf.read(configuration)

        self.hiper = conf["hiper"]
