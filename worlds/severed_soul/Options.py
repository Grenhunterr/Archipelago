import typing
from dataclasses import dataclass
from Options import Option, Range, Toggle, PerGameCommonOptions, DefaultOnToggle


class NotBeingStupid(DefaultOnToggle):
    display_name = "Not Being Stupid"

class OOBCoins(Toggle):
    display_name = "Out of Bounds Coins"

class SecretEndingChecks(Toggle):
    display_name = "Secret Ending Route"

class HiddenSecretChecks(Toggle):
    display_name = "Hidden Secret Checks"

class PPL(Toggle):
    display_name = "Progression Per Level"

class Rando_Claw(Toggle):
    display_name = "Randomize Claw Machine Checks"

class Pit_Checks(Toggle):
    display_name = "Pit Checks (W3L6)"

class Trap_Amount(Range):
    display_name = "Trap Amount"
    range_start = 0
    range_end = 10
    default = 0






@dataclass
class SSOptions(PerGameCommonOptions):
    stupid_people: NotBeingStupid
    secret_ending: SecretEndingChecks
    oob_coins: OOBCoins
    hidden_secret_stuff: HiddenSecretChecks
    progress_per_lvl: PPL
    randomed_claw: Rando_Claw
    i_went_and_fell: Pit_Checks
    traps: Trap_Amount



option_definitions = {
    "stupid_people": NotBeingStupid,
    "secret_ending": SecretEndingChecks,
    "oob_coins": OOBCoins,
    "hidden_secret_stuff": HiddenSecretChecks,
    "progress_per_lvl": PPL,
    "randomed_claw": Rando_Claw,
    "i_went_and_fell": Pit_Checks,
    "traps": Trap_Amount,
}