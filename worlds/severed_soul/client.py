from typing import TYPE_CHECKING
from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class SSClient(BizHawkClient):
    game = "severed_soul"           # Match this with your World name
    system = "GB"                  # SNES, GBA, etc.
    patch_suffix = ".apss"    # Optional: show these files in "Open Patch"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Read some identifying bytes from ROM
            rom_name_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(0x0134, 11, "ROM")])
            rom_name = rom_name_bytes[0].decode("ascii")

            if rom_name != "SEVEREDSOUL":  # Replace with actual expected header or identifier
                return False

        except bizhawk.RequestFailedError:
            return False  # Can't confirm ROM, deny

        # ROM is valid
            ctx.game = self.game
            ctx.items_handling = 0b001  # Server sends items
            ctx.want_slot_data = True
            return True

        async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
            try:
                # Example: Read 16 bytes of RAM at address 0x02000000 (adjust as needed)
                ram_data = (await bizhawk.read(ctx.bizhawk_ctx, [
                    (0x02000000, 16, "EWRAM")
                ]))[0]

                # EXAMPLE: Trigger a location check if bit 3 of byte 0x02000004 is set
                if ram_data[4] & 0x08:  # Bit check: 00001000
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [100010]  # Use your actual Archipelago location ID
                    }])

                # EXAMPLE: Send goal completion when bit 0 of byte 0x02000006 is set
                if not ctx.finished_game and (ram_data[6] & 0x01):
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    ctx.finished_game = True

            except bizhawk.RequestFailedError:
                # BizHawk might have lost connection—just skip this frame
                return
