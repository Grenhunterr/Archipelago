import typing
from dataclasses import dataclass
from Options import Option, Range, Toggle, PerGameCommonOptions, DefaultOnToggle


class NotBeingStupid(DefaultOnToggle):
    display_name = "Not Being Stupid"

class OOBCoins(Toggle):
    display_name = "Out of Bounds Coins"

class SecretEndingChecks(Toggle):
    display_name = "Secret Ending Checks"

class HiddenSecretChecks(Toggle):
    display_name = "Hidden Secret Checks"

class PPL(Toggle):
    display_name = "Progression Per Level"

class Rando_Claw(Toggle):
    display_name = "Randomize Claw Machine Checks"




@dataclass
class SSOptions(PerGameCommonOptions):
    stupid_people: NotBeingStupid
    secret_ending: SecretEndingChecks
    oob_coins: OOBCoins
    hidden_secret_stuff: HiddenSecretChecks
    progress_per_lvl: PPL
    randomed_claw: Rando_Claw



option_definitions = {
    "stupid_people": NotBeingStupid,
    "secret_ending": SecretEndingChecks,
    "oob_coins": OOBCoins,
    "hidden_secret_stuff": HiddenSecretChecks,
    "progress_per_lvl": PPL,
    "randomed_claw": Rando_Claw,
}