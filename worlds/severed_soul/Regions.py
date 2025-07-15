from typing import Optional
from BaseClasses import Region, Entrance
from .Locations import SeveredSoulLocation, location_table


def create_regions(world):
    player = world.player
    multiworld = world.multiworld
    regmen = Region("Menu", player, multiworld, "Menu")
    multiworld.regions.append(regmen)

    regclaw = Region("Claw Machine", player, multiworld, "Claw Machine")
    locclaw_names = ["Claw Machine Interact"]
    if world.options.randomed_claw:
        locclaw_names.append("$5 USD (Claw Machine Draw)")
        locclaw_names.append("Shattered Soul Keychain (Claw Machine Draw)")
        locclaw_names.append("Magic Wand (Claw Machine Draw)")
        locclaw_names.append("Empty Capsule (Claw Machine Draw)")
        locclaw_names.append("Analogue Pocket (Claw Machine Draw)")
        locclaw_names.append("Rock (Claw Machine Draw)")
        locclaw_names.append("Neddy Falti Plushie (Claw Machine Draw)")
        locclaw_names.append("Anchor (Claw Machine Draw)")
        locclaw_names.append("Ghost Keychain (Claw Machine Draw)")
        locclaw_names.append("Star (Claw Machine Draw)")
    regclaw.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regclaw) for loc_name in locclaw_names]
    multiworld.regions.append(regclaw)

    regw1l1 = Region("W1L1", player, multiworld, "W1L1")
    locw1l1_names = ["Coin #1 (W1L1)"]
    regw1l1.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw1l1) for loc_name in locw1l1_names]
    multiworld.regions.append(regw1l1)

    regw1l2 = Region("W1L2", player, multiworld, "W1L2")
    locw1l2_names = ["Coin #1 (W1L2)", "Coin #2 (W1L2)", "Coin #3 (W1L2)", "Coin #4 (W1L2)"]
    if world.options.hidden_secret_stuff:
        locw1l2_names.append("The Eye Sees All")
    regw1l2.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw1l2) for loc_name in locw1l2_names]
    multiworld.regions.append(regw1l2)

    regw1l3 = Region("W1L3", player, multiworld, "W1L3")
    locw1l3_names = ["Coin #1 (W1L3)", "Coin #2 (W1L3)", "Coin #3 (W1L3)", "Coin #4 (W1L3)"]
    regw1l3.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw1l3) for loc_name in locw1l3_names]
    multiworld.regions.append(regw1l3)

    regw2l1 = Region("W2L1", player, multiworld, "W2L1")
    locw2l1_names = ["Coin #1 (W2L1)"]
    regw2l1.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw2l1) for loc_name in locw2l1_names]
    multiworld.regions.append(regw2l1)

    regw2l2 = Region("W2L2", player, multiworld, "W2L2")
    locw2l2_names = ["Coin #1 (W2L2)", "Coin #2 (W2L2)"]
    regw2l2.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw2l2) for loc_name in locw2l2_names]
    multiworld.regions.append(regw2l2)

    regw2l3 = Region("W2L3", player, multiworld, "W2L3")
    locw2l3_names = ["Coin #1 (W2L3)", "Coin #2 (W2L3)"]
    regw2l3.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw2l3) for loc_name in locw2l3_names]
    multiworld.regions.append(regw2l3)

    regw2l4 = Region("W2L4", player, multiworld, "W2L4")
    locw2l4_names = ["Coin #1 (W2L4)", "Coin #2 (W2L4)", "Coin #3 (W2L4)"]
    if world.options.hidden_secret_stuff:
        locw2l4_names.append("Slime-y Secret")
    regw2l4.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw2l4) for loc_name in locw2l4_names]
    multiworld.regions.append(regw2l4)

    regw3l1 = Region("W3L1", player, multiworld, "W3L1")
    locw3l1_names = ["Coin #1 (W3L1)", "Coin #2 (W3L1)", "Coin #3 (W3L1)"]
    regw3l1.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw3l1) for loc_name in locw3l1_names]
    multiworld.regions.append(regw3l1)

    regw3l2 = Region("W3L2", player, multiworld, "W3L2")
    locw3l2_names = ["Coin #1 (W3L2)", "Coin #2 (W3L2)"]
    regw3l2.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw3l2) for loc_name in locw3l2_names]
    multiworld.regions.append(regw3l2)

    regw3l3 = Region("W3L3", player, multiworld, "W3L3")
    locw3l3_names = ["Coin #1 (W3L3)", "Coin #2 (W3L3)", "Coin #3 (W3L3)", "Coin #4 (W3L3)", "Coin #5 (W3L3)"]
    if world.options.oob_coins:
        locw3l3_names.append("Coin #6 (W3L3)")
        if world.options.hidden_secret_stuff:
            locw3l3_names.append("Duck")
    regw3l3.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw3l3) for loc_name in locw3l3_names]
    multiworld.regions.append(regw3l3)

    regw3l4 = Region("W3L4", player, multiworld, "W3L4")
    locw3l4_names = ["Coin #1 (W3L4)", "Coin #2 (W3L4)", "Coin #3 (W3L4)", "Coin #4 (W3L4)"]
    if world.options.oob_coins:
        locw3l4_names.append("Coin #5 (W3L4)")
    regw3l4.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw3l4) for loc_name in locw3l4_names]
    multiworld.regions.append(regw3l4)

    regw3l5 = Region("W3L5", player, multiworld, "W3L5")
    locw3l5_names = ["Coin #1 (W3L5)", "Coin #2 (W3L5)", "Coin #3 (W3L5)", "Coin #4 (W3L5)", "Coin #5 (W3L5)"]
    regw3l5.locations += [SeveredSoulLocation(player, loc_name, location_table[loc_name], regw3l5) for loc_name in locw3l5_names]
    multiworld.regions.append(regw3l5)

    regend = Region("End", player, multiworld, "End")
    multiworld.regions.append(regend)

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


def connect_entrances(world) -> None:
    connect(world, "W1 Entrance (Menu -> W1L1)", "Menu", "W1L1")
    connect(world, "Claw Machine Entrance (Menu -> Claw Machine)", "Menu", "Claw Machine")

    # world connecting
    connect(world, "W2 Entrance (W1L3 -> W2L1)", "W1L3", "W2L1", lambda state: state.has("W2 Key", world.player))
    connect(world, "W3 Entrance (W2L3 -> W3L1)", "W2L3", "W3L1", lambda state: state.has("W3 Key", world.player))
    connect(world, "End Credits Entrance (W3 Exit)", "W3L2", "End", lambda state: state.has("End Credits Key", world.player))

    # level connecting
    connect(world, "W1L1 -> W1L2", "W1L1", "W1L2")
    connect(world, "W1L2 -> W1L3", "W1L2", "W1L3")

    connect(world, "W2L1 -> W2L2", "W2L1", "W2L2")
    connect(world, "W2L2 -> W2L3", "W2L2", "W2L3")
    connect(world, "W2L2 -> W2L4", "W2L2", "W2L4")

    connect(world, "W3L1 -> W3L2", "W3L1", "W3L2")
    connect(world, "W3L2 -> W3L3", "W3L2", "W3L3")
    connect(world, "W3L2 -> W3L4", "W3L2", "W3L4")
    connect(world, "W3L2 -> W3L5", "W3L2", "W3L5")
