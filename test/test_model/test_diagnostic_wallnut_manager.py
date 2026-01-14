# check_wallnut_manager_attributes.py
import pygame
from GardenInvasion.Model.wallnut_model import WallNutManager

pygame.init()

manager = WallNutManager()
print("✅ WallNutManager created successfully")

# Check what attributes it has
print("\nWallNutManager attributes:")
for attr_name in dir(manager):
    if not attr_name.startswith('_'):  # Skip private attributes
        attr_value = getattr(manager, attr_name)
        print(f"  {attr_name}: {type(attr_value).__name__}")

# Specifically check for attributes used in tests
test_attrs = ['player_position', 'screen_width', 'screen_height', 'slot_positions', 'max_wallnuts', 'wallnuts']
print("\nChecking test attributes:")
for attr in test_attrs:
    if hasattr(manager, attr):
        value = getattr(manager, attr)
        print(f"  ✅ {attr}: {value}")
    else:
        print(f"  ❌ {attr}: NOT FOUND")