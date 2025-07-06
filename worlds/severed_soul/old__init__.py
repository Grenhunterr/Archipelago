from BaseClasses import Item, ItemClassification
from . .AutoWorld import World, WebWorld
from .Items import item_table, SeveredSoulItem
from .Locations import location_table, SeveredSoulLocation
from .Options import SSOptions


class SSWeb(WebWorld):
    theme = "stone"


class SSWorld(World):
    game: str = "severed_soul"

    web = SSWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table

    options_dataclass = SSOptions


    def create_item(self, name: str, classification: ItemClassification.filler) -> Item:
        return SeveredSoulItem(name, classification, item_table[name], self.player)

game_name_to_world = {
    "severed_soul": SSWorld,
}


