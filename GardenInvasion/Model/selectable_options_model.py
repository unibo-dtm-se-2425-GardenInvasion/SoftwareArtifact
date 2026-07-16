class SelectableOptionsModel:
    # Shared base for simple two-option selection screens (game over / victory).

    def __init__(self, options):
        self.options = options
        self.selected_index = 0

    def select_next(self):
        # Move selection to the next option
        self.selected_index = (self.selected_index + 1) % len(self.options)

    def select_previous(self):
        # Move selection to the previous option
        self.selected_index = (self.selected_index - 1) % len(self.options)

    def get_selected_option(self) -> str:
        # Return the currently selected option name
        return self.options[self.selected_index]
