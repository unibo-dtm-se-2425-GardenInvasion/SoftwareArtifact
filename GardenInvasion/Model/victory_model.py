from .selectable_options_model import SelectableOptionsModel

class VictoryModel(SelectableOptionsModel):

    def __init__(self):
        super().__init__(["Play Again", "Main Menu"])  # Start with "Play Again" selected
