import pygame
from pathlib import Path
from typing import Optional

class SoundManager:
    # Manages game sound effects with volume control
    
    def __init__(self, settings_model):
        # Initialize sound manager with settings

        if hasattr(settings_model, 'volume'): # Check for valid settings_model
            self.settings_model = settings_model # Use provided settings model
        else:
            # Fallback: Create a simple object with default volume
            print("❌ Warning: Invalid settings_model, using default volume")
            class DefaultSettings: # Simple default settings model
                def __init__(self):
                    self.volume = 50 
            self.settings_model = DefaultSettings() # Use default settings model
        
        self.sounds = {} # Dictionary to hold loaded sounds

        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self._load_sounds() # Load all sound effects
        
        self._update_volume() # Update volume based on settings
    
    def _load_sounds(self):
        # Load all game sound effects from Assets/sounds folder

        pkg_root = Path(__file__).resolve().parent.parent
        sounds_path = pkg_root / "Assets" / "sounds"
        
        # Define sound file mappings
        sound_files = {
            'plant_shoot': 'shoot_plant.wav',  # Sound when plant shoots
            'wallnut_destroyed': 'wallnut_destroyed.wav'  # Sound when wallnut destroyed
        }
        
        # Load each sound file
        for sound_name, filename in sound_files.items(): # Load sounds
            sound_file = sounds_path / filename 
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(str(sound_file)) 
                print(f"✅ Loaded sound: {sound_name}")
            except (pygame.error, FileNotFoundError) as e: # Handle loading errors
                print(f"❌ Warning: Could not load sound '{filename}': {e}")
                self.sounds[sound_name] = None # Silent sound fallback
    
    def _update_volume(self):
        # Update volume for all sounds based on settings

        # Convert 0-100 volume to 0.0-1.0 for pygame
        volume = self.settings_model.volume / 100.0
        
        for sound in self.sounds.values(): # Update volume for each sound
            if sound:
                sound.set_volume(volume)
    
    def play_sound(self, sound_name: str):
        # Play a sound effect
        
        self._update_volume() # Update volume
        
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
        else: # Handle missing sound
            print(f"❌ Sound '{sound_name}' not found or not loaded")
    
    def stop_all(self):
        # Stop all currently playing sounds
        pygame.mixer.stop()
