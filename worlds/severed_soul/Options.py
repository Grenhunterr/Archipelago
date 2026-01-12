import typing
from dataclasses import dataclass
from Options import Option, Range, Toggle, PerGameCommonOptions, DefaultOnToggle, DeathLink, Choice


class NotBeingStupid(DefaultOnToggle):
    """This changes nothing. You can toggle it on or off. Up to your preference"""
    display_name = "Not Being Stupid"

class OOBCoins(Toggle):
    """This toggles coins that are out of bounds. Do not turn this on unless you know where they are."""
    display_name = "Out of Bounds Coins"

# class SecretEndingChecks(Toggle):
#     """Toggles the Secret Ending."""
#     display_name = "Secret Ending Route"

class Which_Route(Choice):
    """Which route will you like to play?"""
    display_name = "Route"
    option_normal = 0
    option_secret = 1
    default = 0

class HiddenSecretChecks(Toggle):
    """Shows the hidden secret stuff. This is seperate from the Secret Ending."""
    display_name = "Hidden Secret Checks"

class PPL(Toggle):
    """SMB3 rules. You need to beat a level to get through the rest of the world."""
    display_name = "Progression Per Level"

class Rando_Claw(Toggle):
    """Randomizes the Claw Machine, which can be found inside the options."""
    display_name = "Randomize Claw Machine Checks"

class Pit_Checks(Toggle):
    """Turns on the checks when falling down a pit in W3L6"""
    display_name = "Pit Checks (W3L6)"
    default = False

class Rude_Client(Toggle):
    """The client WILL talk for you if you turn this on."""
    display_name = "Rude Client"
    default = False


class Trap_Amount(Range):
    """Death Traps :) """
    display_name = "Trap Amount"
    range_start = 0
    range_end = 15
    default = 0

class Pit_Amount(Range):
    """Pit Traps :) """
    display_name = "Pit Amount"
    range_start = 0
    range_end = 5
    default = 0

class Enemy_Hits(Toggle):
    """if you toggle this, you have to get hit by every single enemy."""
    display_name = "Enemy Hits"
    default = False

class Check_Map(Toggle):
    """toggling this will generate a {player}.puml, which is a map of all the obtainable checks inside your Randomization. (only generates on host's machine)"""
    display_name = "Check Map Gen"
    default = False

class Health_items(Toggle):
    """...would you like to heal or nah?"""
    display_name = "Health Items"
    default = True

class More_Coins(Toggle):
    """toggling this activates the items '2 Coins' and '10 Coins'. don't worry, it will still cap out at 255"""
    display_name = "More Coins"
    default = False

class Look_Under_The_Hood(Toggle):
    """Turns on a bunch of prints while generating so you can see what's happening"""
    display_name = "Behind The Scenes"
    default = False

class Secret_Shop(Toggle):
    """secret shop? what are you talking about? I never saw something like that... weird timeline this is. (don't turn this on just yet, it's broken)"""
    display_name = "Secret Shop"
    default = False

class FunnyDeath(Toggle):
    """gives random death messages which replace the original ones."""
    display_name = "Funny Death Messages"
    default = False

@dataclass
class SSOptions(PerGameCommonOptions):
    route: Which_Route
    oob_coins: OOBCoins
    hidden_secret_stuff: HiddenSecretChecks
    progress_per_lvl: PPL
    randomed_claw: Rando_Claw
    i_went_and_fell: Pit_Checks
    traps: Trap_Amount
    pit_traps: Pit_Amount
    enemy_hits: Enemy_Hits
    death_link: DeathLink
    health_items: Health_items
    more_coins: More_Coins
    secret_shop: Secret_Shop




option_definitions = {
    "stupid_people": NotBeingStupid,
    "route": Which_Route,
    "oob_coins": OOBCoins,
    "hidden_secret_stuff": HiddenSecretChecks,
    "progress_per_lvl": PPL,
    "randomed_claw": Rando_Claw,
    "i_went_and_fell": Pit_Checks,
    "traps": Trap_Amount,
    "rude_client": Rude_Client,
}