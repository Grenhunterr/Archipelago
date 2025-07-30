import settings
import typing
from .Options import SSOptions  # the options we defined earlier
from .Items import SeveredSoulItem, item_table  # data used below to add items to the World
from .Locations import SeveredSoulLocation, location_table  # same as above
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, MultiWorld
from .Regions import create_regions, connect_entrances
from .client import SSClient




class MyGameSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """Insert help text for host.yaml here."""
        #rom_file: RomFile = RomFile("SSAP.gb")
        description =  "Severed Souls AP ROM"
        copy_to = "Severed Soul AP ROM which is totally legit and fully functioning.gb"
        md5s = ["E9773D4BE958C4C00C8E7A740554C563"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True



class SeveredSoulWeb(WebWorld):
    theme = "stone"
    options_presets = {
        "Severed Soul": {
            "stupid_people": True,
            "secret_ending": False,
            "oob_coins": False,
            "hidden_secret_stuff": False,
            "progress_per_lvl": False,
        }
    }


class SeveredSoulWorld(World):
    """2D Platformer for the Game Boy! (Copywrite Grenhunterr 2024)"""
    game = "severed_soul"  # name of the game/world
    options_dataclass = SSOptions  # options the player can set
    options: SSOptions  # typing hints for option results
    settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
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
        "keys": {"W2 Key", "W3 Key", "End Credits Key", "Claw Machine Key"},
        "coins": {"Coin"}
    }


    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)



    def create_regions(self):
        create_regions(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("End", "Region", self.player) and state.has("End Credits Key", self.player)



    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):

        totalItems = len(self.multiworld.get_unfilled_locations(self.player))


        # add regular items
        for k, v in item_table.items():
            item = Item(k, ItemClassification.progression, self.item_name_to_id[k], self.player)

            self.multiworld.itempool.append(item)
            totalItems -= 1
        for _ in range(totalItems):
            item = Item("Coin", ItemClassification.filler, 2010004, self.player)
            self.multiworld.itempool.append(item)


    def connect_entrances(self) -> None:
        connect_entrances(self)
#        from Utils import visualize_regions
#        visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_world.puml",
#                          show_entrance_names=True,
#                          regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
#                              self.player])

