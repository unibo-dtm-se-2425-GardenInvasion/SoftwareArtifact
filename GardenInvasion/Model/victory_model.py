class VictoryModel:
    
    def __init__(self):
        self.options = ["Play Again", "Main Menu"]
        self.selected_index = 0  # Start with "Play Again" selected
    
    def select_next(self):
        # Move selection to the right
        self.selected_index = (self.selected_index + 1) % len(self.options)
    
    def select_previous(self):
        # Move selection to the left
        self.selected_index = (self.selected_index - 1) % len(self.options)
    
    def get_selected_option(self):
        return self.options[self.selected_index]
