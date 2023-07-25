"""Configuration module"""
import os
from configparser import ConfigParser
from dataclasses import dataclass, field

from click import ClickException

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

    hiper: dict = field(init=False)

    def __post_init__(self):
        home = os.path.expanduser("~")

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
