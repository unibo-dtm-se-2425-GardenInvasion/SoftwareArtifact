import pygame
from pathlib import Path
from typing import Optional 
import os

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

        self.sounds= {} # Dictionary to hold sound effects
        self.music_tracks = {}  # Dictionary to hold music file paths
        self.current_music = None  # Track currently playing music

        self.audio_available = True
        
        # Check if running in CI or headless environment
        if os.environ.get('SDL_AUDIODRIVER') == 'dummy' or os.environ.get('CI'):
            print("Running in headless environment, audio disabled")
            self.audio_available = False
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                # Try to initialize with dummy driver if needed
                if not self.audio_available:
                    os.environ['SDL_AUDIODRIVER'] = 'dummy'
                
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                # print("Audio initialized successfully")
            except pygame.error as e:
                print(f"Audio initialization failed: {e}")
                self.audio_available = False
                # Set dummy driver and try again
                os.environ['SDL_AUDIODRIVER'] = 'dummy'
                try:
                    pygame.mixer.init()
                except:
                    pass
        
        self._load_sounds() # Load all sound effects
        self._load_music() # Load music tracks
        
        self._update_volume() # Update volume based on settings
    
    def _load_sounds(self):
        # Load all game sound effects

        if not self.audio_available:
            print("Skipping sound loading -> no audio")
            return

        pkg_root = Path(__file__).resolve().parent.parent
        sounds_path = pkg_root / "Assets" / "sounds"
        
        # Define sound file mappings
        sound_files = {
            'plant_shoot': 'shoot_plant.wav',  # Sound when plant shoots
            'wallnut_destroyed': 'wallnut_destroyed.wav',  # Sound when wallnut destroyed
            'game_over': 'gameover_sound.ogg'  # Game over sound   
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

        if not self.audio_available:
            print("Skipping music loading -> no audio")
            return
        
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

        if not self.audio_available: # No audio available
            return

        volume = self.settings_model.volume / 100.0 # Convert to 0.0 - 1.0 range
        
        for sound in self.sounds.values(): # Update volume for each sound
            if sound:
                sound.set_volume(volume)

        try:
            pygame.mixer.music.set_volume(volume)
        except:
            pass
    
    def play_sound(self, sound_name: str):
        # Play a sound effect

        if not self.audio_available:
            return
        
        self._update_volume()
        
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
        else: # Handle missing sound
            print(f"Sound '{sound_name}' not found or not loaded")

    def play_music(self, music_name: str, loops: int = -1, fade_ms: int = 1000):
        # Play background music (looping by default)

        if not self.audio_available: 
            return        
        
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

        if not self.audio_available:
            return
        try:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(fade_ms)
            else:
                pygame.mixer.music.stop()
        except:
            pass
        
        self.current_music = None # Clear currently playing music
        # print("Music stopped") # Log music stop
    
    def pause_music(self):
        # Pause the currently playing music
        if not self.audio_available:
            return
        try:
            pygame.mixer.music.pause()
            # print("Music paused")
        except:
            pass
    
    def unpause_music(self):
        # Resume paused music
        if not self.audio_available:
            return
        try:
            pygame.mixer.music.unpause()
            # print("Music resumed")
        except:
            pass
    
    def stop_all(self):
        # Stop all currently playing sounds
        if not self.audio_available:
            return
        try:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            self.current_music = None
        except:
            pass

    def update_volume_realtime(self):
        self._update_volume() # Update volume based on current settings in real-time
 
