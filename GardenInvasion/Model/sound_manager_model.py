import pygame
from pathlib import Path
from typing import Optional

class SoundManager:
    # Manages game sound effects with volume control
    def __init__(self, settings_model):
        if hasattr(settings_model, 'volume'): # Check for valid settings_model
            self.settings_model = settings_model # Use provided settings model
        else:
            # Fallback: Create a simple object with default volume
            print("Warning: Invalid settings_model, using default volume")
            class DefaultSettings: # Simple default settings model
                def __init__(self):
                    self.volume = 50 
            self.settings_model = DefaultSettings() # Use default settings model
        
        self.sounds = {} # Dictionary to hold loaded sounds

        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.music_tracks = {}  # Dictionary to hold music file paths
        self.current_music = None  # Track currently playing music
        
        self._load_sounds() # Load all sound effects
        self._load_music() # Load music tracks
        
        self._update_volume() # Update volume based on settings
    
    def _load_sounds(self):
        # Load all game sound effects

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
                # print(f"Loaded sound: {sound_name}")
            except (pygame.error, FileNotFoundError) as e: # Handle loading errors
                print(f"Warning: Could not load sound '{filename}': {e}")
                self.sounds[sound_name] = None # Silent sound fallback

    def _load_music(self):
        # Load background music file
        
        pkg_root = Path(__file__).resolve().parent.parent
        music_path = pkg_root / "Assets" / "sounds"
        
        # Define music file mappings
        music_files = {
            'menu': 'menu_soundtrack.ogg',      # Menu background music
            'gameplay': 'rungame_soundtrack.mp3'  # Gameplay background music
        }
        
        # Store music file paths
        for music_name, filename in music_files.items():
            music_file = music_path / filename
            if music_file.exists(): # Check if file exists
                self.music_tracks[music_name] = str(music_file) # Store file path
                # print(f"Found music track: {music_name}")
            else:
                print(f"Warning: Music file not found: {filename}") 
                self.music_tracks[music_name] = None # No file available
        
    def _update_volume(self):
        # Update volume for all sounds based on settings

        volume = self.settings_model.volume / 100.0 # Convert to 0.0 - 1.0 range
        
        for sound in self.sounds.values(): # Update volume for each sound
            if sound:
                sound.set_volume(volume)

        pygame.mixer.music.set_volume(volume) # Update music volume too
    
    def play_sound(self, sound_name: str):
        # Play a sound effect
        
        self._update_volume()
        
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
        else: # Handle missing sound
            print(f"Sound '{sound_name}' not found or not loaded")

    def play_music(self, music_name: str, loops: int = -1, fade_ms: int = 1000):
        # Play background music (looping by default)
        
        
        if self.current_music == music_name and pygame.mixer.music.get_busy(): # If same music is already playing, don't restart
            return
        
        if music_name in self.music_tracks and self.music_tracks[music_name]: # Check if music track exists
            try:
                pygame.mixer.music.load(self.music_tracks[music_name])
                self._update_volume()  # Set volume before playing
                pygame.mixer.music.play(loops=loops, fade_ms=fade_ms) # Play music with fade-in
                self.current_music = music_name # Update currently playing music
                # print(f" Playing music: {music_name}")
            except pygame.error as e: # Handle loading/playing errors
                print(f" Could not play music '{music_name}': {e}")
        else:
            print(f" Music track '{music_name}' not found") # Handle missing music track
    
    def stop_music(self, fade_ms: int = 1000):
        # Stop background music with optional fade out
        
        if fade_ms > 0: # Fade out if specified
            pygame.mixer.music.fadeout(fade_ms) # Fade out music
        else: # Immediate stop
            pygame.mixer.music.stop() # Stop music immediately
        self.current_music = None # Clear currently playing music
        # print("Music stopped") # Log music stop
    
    def pause_music(self):
        # Pause the currently playing music
        pygame.mixer.music.pause() # Pause music playback
    
    def unpause_music(self):
        # Resume paused music
        pygame.mixer.music.unpause() # Resume music playback
    
    def stop_all(self):
        # Stop all currently playing sounds
        pygame.mixer.stop()

    def update_volume_realtime(self):
        self._update_volume() # Update volume based on current settings in real-time
 
