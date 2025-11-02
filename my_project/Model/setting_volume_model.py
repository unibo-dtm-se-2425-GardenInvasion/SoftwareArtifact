import json
import os

class SettingsModel:
    # Model to store user settings persistently.
    # Manages loading/saving settings like volume from/to a JSON file.
    
    SETTINGS_FILENAME = 'settings.json'

    def __init__(self):
        # Default volume setting
        self.volume = 50
        # Store settings file path in user home or app directory
        self._filepath = os.path.join(os.path.expanduser('~'), '.garden_invasion_settings.json')

    def load(self):
        # Load settings from JSON file.
        # If file doesn't exist, defaults are used.
        
        try:
            with open(self._filepath, 'r') as f:
                data = json.load(f)
                self.volume = data.get('volume', 50)
        except FileNotFoundError:
            # Settings file does not exist, keep defaults
            pass

    def save(self):
        # Save current settings to JSON file.
        data = {'volume': self.volume}
        with open(self._filepath, 'w') as f:
            json.dump(data, f)

