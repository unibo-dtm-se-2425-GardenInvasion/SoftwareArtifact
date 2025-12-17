import unittest
import os
import json
import tempfile
from GardenInvasion.Model.options_model import OptionsModel, VolumeModel
from GardenInvasion.Model.setting_volume_model import SettingsModel


class TestOptionsModel(unittest.TestCase):
    """Test suite for OptionsModel class"""

    def test_initial_options_items_list(self):
        #Test that OptionsModel initializes with correct options items
        
        model = OptionsModel()
        # Verify options_items is a list with 4 items
        self.assertIsInstance(model.options_items, list)
        self.assertEqual(len(model.options_items), 4)
        print(f"✅ OptionsModel initialized with {len(model.options_items)} items")

    def test_options_items_contains_volume(self):
        #Test that options_items contains 'Volume'
        
        model = OptionsModel()
        # Verify "Volume" is in the options items
        self.assertIn("Volume", model.options_items)
        print("✅ OptionsModel contains 'Volume' option")

    def test_options_items_contains_contact_us(self):
        #Test that options_items contains 'Contact Us'

        model = OptionsModel()
        # Verify "Contact Us" is in the options items
        self.assertIn("Contact Us", model.options_items)
        print("✅ OptionsModel contains 'Contact Us' option")

    def test_options_items_contains_back(self):
        #Test that options_items contains 'Back'
        
        model = OptionsModel()
        # Verify "Back" is in the options items
        self.assertIn("Back", model.options_items)
        print("✅ OptionsModel contains 'Back' option")


class TestVolumeModel(unittest.TestCase):
    """Test suite for VolumeModel class"""

    def test_initial_volume_custom_value(self):
        #Test that VolumeModel accepts custom initial volume
        
        # Create VolumeModel with custom initial volume
        custom_volume = 75
        model = VolumeModel(initial_volume=custom_volume)
        # Verify volume is set to the custom value
        self.assertEqual(model.volume, custom_volume)
        print(f"✅ VolumeModel accepted custom initial volume: {custom_volume}")

    def test_volume_accepts_zero(self):
        #Test that VolumeModel accepts volume of 0 (muted)
        
        model = VolumeModel(initial_volume=0)
        # Verify volume is 0
        self.assertEqual(model.volume, 0)
        print("✅ VolumeModel accepted volume = 0 (muted)")

    def test_volume_accepts_hundred(self):
        #Test that VolumeModel accepts volume of 100 (maximum)
        
        model = VolumeModel(initial_volume=100)
        # Verify volume is 100
        self.assertEqual(model.volume, 100)
        print("✅ VolumeModel accepted volume = 100 (maximum)")


class TestSettingsModel(unittest.TestCase):
    """Test suite for SettingsModel class"""

    def setUp(self):
        """Set up test fixtures before each test"""
        
        # Create a SettingsModel instance
        self.model = SettingsModel()
        # Store original filepath
        self.original_filepath = self.model._filepath
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        # Override the filepath to use temp file
        self.model._filepath = self.temp_file.name

    def tearDown(self):
        """Clean up after each test"""
        # Remove temporary file if it exists
        try:
            os.remove(self.temp_file.name)
        except FileNotFoundError:
            pass

    def test_filepath_contains_home_directory(self):
        """Test that settings filepath includes user home directory"""
        # Create a fresh SettingsModel to check original filepath
        model = SettingsModel()
        
        # Get user home directory
        home_dir = os.path.expanduser('~')
        
        # Verify filepath contains home directory
        self.assertIn(home_dir, model._filepath)
        print(f"✅ Settings filepath contains home directory: {home_dir}")

    def test_filepath_contains_garden_invasion(self):
        #Test that settings filepath contains 'garden_invasion'
        
        # Create a fresh SettingsModel
        model = SettingsModel()
        # Verify filepath contains 'garden_invasion'
        self.assertIn('garden_invasion', model._filepath)
        print("✅ Settings filepath contains 'garden_invasion'")

    def test_load_reads_existing_file(self):
        #Test that load() reads volume from existing file

        # Write test data to file
        test_volume = 75
        with open(self.temp_file.name, 'w') as f:
            json.dump({'volume': test_volume}, f)
        
        self.model.load()
        # Verify volume was read correctly
        self.assertEqual(self.model.volume, test_volume)
        print(f"✅ load() successfully read volume from file: {test_volume}")

    def test_save_creates_json_file(self):
        #Test that save() creates a JSON file"""
        
        #Remove file if it exists
        try:
            os.remove(self.temp_file.name)
        except FileNotFoundError:
            pass
        
        self.model.save()
        # Verify file was created
        self.assertTrue(os.path.exists(self.temp_file.name))
        print("✅ save() created JSON file successfully")

    def test_save_writes_volume_to_file(self):
        #Test that save() writes current volume to file
        
        test_volume = 85
        self.model.volume = test_volume
        self.model.save()
        # Read file and verify content
        with open(self.temp_file.name, 'r') as f:
            data = json.load(f)
        
        # Verify volume was saved correctly
        self.assertEqual(data['volume'], test_volume)
        print(f"✅ save() wrote volume to file: {test_volume}")


if __name__ == '__main__':
    unittest.main()
