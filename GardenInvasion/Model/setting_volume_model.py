import json
import os

class SettingsModel:
    # Model to store user settings persistently.
    # Manages loading/saving settings like volume from/to a JSON file.
    
    SETTINGS_FILENAME = 'settings.json'

    def __init__(self):
        # Default volume setting
        self.volume = 50
        self.player_skin = "default"  # Default player skin ID
        # Store settings file path in user home or app directory
        self._filepath = os.path.join(os.path.expanduser('~'), '.garden_invasion_settings.json')

    def load(self):
        # Load settings from JSON file.
        # If file doesn't exist, defaults are used.
        
        try:
            with open(self._filepath, 'r') as f:
                data = json.load(f)
                self.volume = data.get('volume', 50)
                self.player_skin = data.get('player_skin', 'default')  # Load skin, default to "default"
        except FileNotFoundError:
            # Settings file does not exist
            pass
        except json.JSONDecodeError:
            # Corrupted settings file
            pass
    def save(self):
        # Save current settings to JSON file.
        data = {
            'volume': self.volume, # add volume to saved data
            'player_skin': self.player_skin  # Add player_skin to saved data
        }
        with open(self._filepath, 'w') as f:
            json.dump(data, f, indent=4)

