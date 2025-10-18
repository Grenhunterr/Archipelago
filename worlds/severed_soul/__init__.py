import settings
import typing

from Options import OptionError
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
    game = "Severed Soul"  # name of the game/world
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
        "keys": {"W2 Key", "W3 Key", "End Credits Key", "Claw Machine Key", "Mysterious Key"},
        "coins": {"Coin"},
        "secrets": {"Secret Item #1", "Secret Item #2", "Secret Item #3", "Secret Item #4"}
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
        self.multiworld.itempool.append(Item("W2 Key", ItemClassification.progression, self.item_name_to_id["W2 Key"], self.player))
        self.multiworld.itempool.append(Item("W3 Key", ItemClassification.progression, self.item_name_to_id["W3 Key"], self.player))
        self.multiworld.itempool.append(Item("End Credits Key", ItemClassification.progression, self.item_name_to_id["End Credits Key"], self.player))
        self.multiworld.itempool.append(Item("Claw Machine Key", ItemClassification.progression, self.item_name_to_id["Claw Machine Key"], self.player))
        totalItems -= 4

        if self.options.secret_shop:
            self.multiworld.itempool.append(Item("Mysterious Key", ItemClassification.progression, self.item_name_to_id["Mysterious Key"], self.player))
            totalItems -= 1


        if self.options.secret_ending == True:
            self.multiworld.itempool.append(
                Item("Secret Item #1", ItemClassification.progression, self.item_name_to_id["Secret Item #1"], self.player))
            self.multiworld.itempool.append(
                Item("Secret Item #2", ItemClassification.progression, self.item_name_to_id["Secret Item #2"], self.player))
            self.multiworld.itempool.append(
                Item("Secret Item #3", ItemClassification.progression, self.item_name_to_id["Secret Item #3"], self.player))
            self.multiworld.itempool.append(
                Item("Secret Item #4", ItemClassification.progression, self.item_name_to_id["Secret Item #4"], self.player))
            totalItems -= 4





        progCoins = totalItems // 2 if self.options.randomed_claw else 0
        if not self.options.more_coins:
            for _ in range(progCoins):
                item = Item("Coin", ItemClassification.progression, 2010004, self.player)
                self.multiworld.itempool.append(item)
                totalItems -= 1


        for _ in range(self.options.traps):
            self.multiworld.itempool.append(Item("Death (Trap)", ItemClassification.trap, self.item_name_to_id["Death (Trap)"], self.player))
            totalItems -= 1

        for _ in range(self.options.pit_traps):
            self.multiworld.itempool.append(Item("Pitfallin' Time! (Trap)", ItemClassification.trap, self.item_name_to_id["Pitfallin' Time! (Trap)"], self.player))
            totalItems -= 1

        coinsforclaw = totalItems // 3 if self.options.more_coins and self.options.randomed_claw else 0
        coinsgalore = totalItems // 5 if self.options.more_coins else 0

        for _ in range(coinsforclaw):
            item = Item("10 Coins", ItemClassification.progression, 2010013, self.player)
            self.multiworld.itempool.append(item)
            totalItems -= 1

        for _ in range(coinsgalore):
            if self.options.more_coins:
                item = Item("2 Coins", ItemClassification.useful, 2010013, self.player)
                self.multiworld.itempool.append(item)
                totalItems -= 1
            else:
                item = Item("2 Coins", ItemClassification.filler, 2010013, self.player)
                self.multiworld.itempool.append(item)
                totalItems -= 1

        totHeals = totalItems // 4 if self.options.health_items else 0

        for _ in range(totHeals):
            item = Item("+1 Health", ItemClassification.useful, 2010011, self.player)
            self.multiworld.itempool.append(item)
            totalItems -= 1

        for _ in range(totHeals):
            item = Item("+2 Health", ItemClassification.useful, 2010012, self.player)
            self.multiworld.itempool.append(item)
            totalItems -= 1


        for _ in range(totalItems):
            item = Item("Coin", ItemClassification.filler, 2010004, self.player)
            self.multiworld.itempool.append(item)



    def connect_entrances(self) -> None:
        connect_entrances(self)
        if self.options.puml_gen:

            from Utils import visualize_regions
            visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_SeveredSoul_world.puml",
                            show_entrance_names=True,
                            regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
                                self.player])

    def fill_slot_data(self) -> dict[str, any]:
        # In order for our game client to handle the generated seed correctly we need to know what the user selected
        # for their difficulty and final boss HP.
        # A dictionary returned from this method gets set as the slot_data and will be sent to the client after connecting.
        # The options dataclass has a method to return a `Dict[str, Any]` of each option name provided and the relevant
        # option's value.
        names = ["progress_per_lvl", "secret_ending", "hidden_secret_stuff", "stupid_people", "death_link", "rude_client"]
        return self.options.as_dict(*names)