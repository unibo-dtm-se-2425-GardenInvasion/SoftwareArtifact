class GameOverModel:
    # Model for game over screen state
    
    def __init__(self):
        self.options = ["Start Again", "Main Menu"]  # Game over options
        self.selected_index = 0  # Index of currently selected option (0=Start Again, 1=Main Menu)
    
    def select_next(self):
        # Move selection to the next option
        self.selected_index = (self.selected_index + 1) % len(self.options)
    
    def select_previous(self):
        # Move selection to the previous option
        self.selected_index = (self.selected_index - 1) % len(self.options)
    
    def get_selected_option(self) -> str:
        # Return the currently selected option name
        return self.options[self.selected_index]
    
    def reset(self):
        # Reset selection to first option
        self.selected_index = 0
