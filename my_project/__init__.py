import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('my_project')

# this is the initial module of your app
# this is executed whenever some client-code is calling `import my_project` or `from my_project import ...`
# put your main classes here, eg:
class MyClass:
    def my_method(self):
        return "Hello fellow plant, get ready to defend yourself from zombies soon"
    
try:
    from .engine.game_engine import GameEngine
    __all__ = ["GameEngine"]
except ImportError:
    __all__ = []

# let this be the last line of this file
logger.info("Garden Invasion loaded")
