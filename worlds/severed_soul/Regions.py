import typing
from BaseClasses import MultiWorld, Region
from .Locations import SeveredSoulLocation, location_table


def create_regions(world: MultiWorld, player: int):
    regmen = Region("Menu", player, world, "Menu")
    world.regions.append(regmen)


    regw1l1 = Region("W1L1", player, world, "W1L1")
    locw1l1_names = ["Coin #1 (W1L1)"]
    regw1l1.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw1l1) for loc_name in locw1l1_names]
    world.regions.append(regw1l1)