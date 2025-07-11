from typing import Optional
from BaseClasses import MultiWorld, Region, Entrance
from .Locations import SeveredSoulLocation, location_table


def create_regions(world: MultiWorld, player: int):
    regmen = Region("Menu", player, world, "Menu")
    world.regions.append(regmen)


    regw1l1 = Region("W1L1", player, world, "W1L1")
    locw1l1_names = ["Coin #1 (W1L1)"]
    regw1l1.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw1l1) for loc_name in locw1l1_names]
    world.regions.append(regw1l1)

    regw1l2 = Region("W1L2", player, world, "W1L2")
    locw1l2_names = ["Coin #1 (W1L2), Coin #2 (W1L2), Coin #3 (W1L2)"]
    regw1l2.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw1l2) for loc_name in locw1l2_names]
    world.regions.append(regw1l2)



















def connect(world, name: str, source: str, target: str, rule=None, reach: Optional[bool] = False,
            rule_to_str: Optional[str] = None, ) -> Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)

    print(f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n")

    return connection if reach else None