import settings
import typing
from .Options import SSOptions  # the options we defined earlier
from .Items import SeveredSoulItem, item_table  # data used below to add items to the World
from .Locations import SeveredSoulLocation, location_table  # same as above
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from .Regions import create_regions

#class MyGameSettings(settings.Group):
#   class RomFile(settings.GBRomPath):
#       """Insert help text for host.yaml here."""
#   rom_file: RomFile = RomFile("SeveredSoul-V1.1.gb")


class SeveredSoulWorld(World):
    """2D Platformer for the Game Boy! (Copywrite Grenhunterr 2024)"""
    game = "severed_soul"  # name of the game/world
    options_dataclass = SSOptions  # options the player can set
    options: SSOptions  # typing hints for option results
#    settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = False  # show path to required location checks in spoiler





    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 2010
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       name, id in item_table.items()}
    location_name_to_id = {name: id for
                           name, id in location_table.items()}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        "keys": {"W2 Key", "W3 Key"},
    }




    def create_regions(self):
        create_regions(self.multiworld, self.player)


    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)



    def create_items(self):
        # create item pool
        pool = []

        # add regular items
        for k, v in item_table.items():
            item = Item(k, ItemClassification.progression, self.item_name_to_id[k], self.player)

            self.multiworld.itempool.append(item)


    def connect_entrances(self) -> None:
        