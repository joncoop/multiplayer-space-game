# Standard Library Imports

# Third-Party Imports

# # Local imports
import settings
from .entity import Item


class ShieldBoost(Item):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def apply(self, ship):
        ship.shield += 1


class DoubleShot(Item):

    def __init__(self, game, image, location):
        super().__init__(game, image, location)

    def apply(self, ship):
        ship.doubleshot_time = settings.DOUBLE_SHOT_TIME
