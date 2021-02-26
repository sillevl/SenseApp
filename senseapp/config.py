import json
import os.path
import warnings
from pathlib import Path

# application settings
default_settings = {
    "wanted_temperature": 36.0,
    "wanted_temperature_range": 1.0,
    "brightness": 255,
    "low_light": False,
    "display_speed": 0.075,
    "rotation": 180
}

SETTINGS_PATH = "/etc/senseapp"
SETTINS_FILE = "settings.json"

class Manager:

    path = None
    settings = dict()
    on_update_callback = None

    def __init__(self, path="/etc/senseapp/settings.json"):
        # os.path.join(SETTINGS_PATH, SETTINS_FILE)
        self.path = path
        self.create_file_if_not_exists()
        self.settings = self.read()


    def create_file_if_not_exists(self):
        Path(SETTINGS_PATH).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w') as outfile:
                json.dump(default_settings, outfile, indent=2)

    def read(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
            settings = { **default_settings, **data }
            return settings

    def save(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.settings, outfile, indent=2)
        # print(f"Settings updated: {self.settings}")

    def set(self, setting, value):
        if setting not in self.settings.keys():
            raise Warning(f"Setting {setting} does not exist ({self.settings})")
        self.settings[setting] = value
        self.__update(setting, value)
        self.save()

    def get(self, setting):
        if setting not in self.settings.keys():
            raise Warning(f"Setting {setting} does not exist")
        return self.settings[setting]
    
    def get_all(self):
        return self.settings

    def set_all(self, settings):
        for key, value in settings.items():
            try:
                self.set(key, value)
            except:
                print(f"Settings does not contain a key {key}")
        print(f"Settings updated: {self.settings}")

    def __update(self, key, value):
        if self.on_update_callback:
            self.on_update_callback(key, value)

    def on_update(self, callback):
        self.on_update_callback = callback