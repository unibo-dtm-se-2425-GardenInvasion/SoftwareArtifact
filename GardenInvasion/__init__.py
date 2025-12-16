import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('GardenInvasion')

# this is the initial module of your app
# this is executed whenever some client-code is calling `import GardenInvasion` or `from GardenInvasion import ...`
# put your main classes here, eg:
class MyClass:
    def my_method(self):
        return "Hello fellow plant, get ready to defend yourself from zombies soon"

# let this be the last line of this file
logger.info("Garden Invasion loaded")
