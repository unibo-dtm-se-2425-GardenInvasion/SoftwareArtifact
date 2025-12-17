class OptionsModel:
    def __init__(self):
        self.options_items = ["Volume", "Skin Personalization", "Contact Us", "Back"] # List of option items
        self.selected_index = 0
        self.volume = 50
        self.modal_selected_button = 0

class VolumeModel:
    def __init__(self, initial_volume: int = 50):
        self.volume = initial_volume # Volume level from 0 to 100
