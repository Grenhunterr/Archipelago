from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class SeveredSoulClient(BizHawkClient):
    game = "severed_soul"
    system = "GB"  # Original Game Boy
    patch_suffix = ".apextension"  # Keeping this as-is

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x100, 11, "ROM")]))[0]).decode("latin-1")
            if rom_name.strip() != "SEVEREDSOUL":
                return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            memory = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x0B98, 1, "System Bus"),  # coins
                    (0x0B94, 1, "System Bus"),  # lives
                    (0x0B9C, 1, "System Bus"),  # secret item
                    (0x0BA4, 1, "System Bus"),  # ending trigger
                ]
            )

            coins = memory[0][0]
            lives = memory[1][0]
            secret_item = memory[2][0]
            ending_flag = memory[3][0]

            # Example location check: collected secret item
            if secret_item != 0:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [100]  # Update this with your actual location ID
                }])

            # Game finished check
            if not ctx.finished_game and ending_flag != 0:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            pass
