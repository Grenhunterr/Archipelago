import typing
from dataclasses import dataclass
from Options import Option, Range, Toggle, PerGameCommonOptions

class NotBeingStupid(Toggle):
    display_name = "Not Being Stupid"


@dataclass
class SSOptions(PerGameCommonOptions):
    stupid_people: NotBeingStupid



option_definitions = {
    "stupid_people": NotBeingStupid
}