"""CLI Session module"""

import os
from dataclasses import dataclass, field

from timekeeper.config import Config
from timekeeper.model import Session, Times


@dataclass
class CliSession:
    """Session object for CLI interface"""

    config: Config = field(init=False)
    times_model: Times = field(init=False)

    def __post_init__(self):
        self.config = Config()

        home = os.path.expanduser("~")
        database = os.path.join(home, "timekeeper.db")

        self.times_model = Times(database)
        self.session_model = Session(database)
