from .selectable_options_model import SelectableOptionsModel

class GameOverModel(SelectableOptionsModel):
    # Model for game over screen state

    def __init__(self):
        super().__init__(["Start Again", "Main Menu"])  # Game over options

    def reset(self):
        # Reset selection to first option
        self.selected_index = 0
