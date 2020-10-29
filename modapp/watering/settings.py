from . import APPNAME, VERSION
from modcore.log import LogSupport, logger
from modext.config import Config, ReprDict


##todo
## fefractor own modcore module reboot


class Settings(ReprDict, LogSupport):
    def __init__(self):
        self.app = APPNAME
        self.version = VERSION
        self.load()

    def load(self):
        settings_cfg = Config("/etc/" + self.app + "/settings.json.txt")
        try:
            settings_cfg.load()
        except:
            ## todo logging
            # no config found, load defaults
            settings_cfg.load("/modapp/" + self.app + "/etc/settings.template.json.txt")

        self._config = settings_cfg

    def save(self):
        self._config.save()

    def config(self):
        return self._config

    def __repr__(self):
        return {
            "settings": self._config,
            "app": self.app,
            "version": self.version,
        }


mod_settings = Settings()
