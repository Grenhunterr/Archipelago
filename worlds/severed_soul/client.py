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
            print(rom_name)

            if rom_name != "SEVEREDSOUL":  # Replace with actual expected header or identifier
                return False
            ctx.game = self.game
            ctx.items_handling = 0b001  # Server sends items
            ctx.want_slot_data = True
            return True
        except bizhawk.RequestFailedError:
            return False  # Can't confirm ROM, deny

        # ROM is valid


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Read necessary WRAM bytes from memory
            ram_data = (await bizhawk.read(ctx.bizhawk_ctx, [
                (0x0BA4, 1, "WRAM"),  # Release
                (0x0BAE, 1, "WRAM"),  # Claw Machine Interact
                (0x0BB2, 1, "WRAM"),
                (0x0BB4, 1, "WRAM"),
                (0x0BB6, 1, "WRAM"),
                (0x0BB8, 1, "WRAM"),
                (0x0BBA, 1, "WRAM"),
                (0x0BBC, 1, "WRAM"),
                (0x0BBE, 1, "WRAM"),
                (0x0BC0, 1, "WRAM"),
                (0x0BC2, 1, "WRAM"),
                (0x0BC4, 1, "WRAM"),
                (0x0BC6, 1, "WRAM"),
                (0x0BC8, 1, "WRAM"),
                (0x0BCA, 1, "WRAM"),
                (0x0BCC, 1, "WRAM"),
                (0x0BCE, 1, "WRAM"),
                (0x0BD0, 1, "WRAM"),
                (0x0BD2, 1, "WRAM"),
                (0x0BD4, 1, "WRAM"),
                (0x0BD6, 1, "WRAM"),
                (0x0BD8, 1, "WRAM"),
                (0x0BDC, 1, "WRAM"),
                (0x0BDE, 1, "WRAM"),
                (0x0BE0, 1, "WRAM"),
                (0x0BE2, 1, "WRAM"),
                (0x0BE4, 1, "WRAM"),
                (0x0BE6, 1, "WRAM"),
                (0x0BE8, 1, "WRAM"),
                (0x0BEA, 1, "WRAM"),
                (0x0BEC, 1, "WRAM"),
                (0x0BEE, 1, "WRAM"),
                (0x0BF0, 1, "WRAM"),
                (0x0BF2, 1, "WRAM"),
                (0x0BF4, 1, "WRAM"),
                (0x0BF6, 1, "WRAM"),
                (0x0BF8, 1, "WRAM"),
                (0x0BFA, 1, "WRAM"),
                (0x0BFC, 1, "WRAM"),
                (0x0BFE, 1, "WRAM"),  # Slime-y Secret
                (0x0C00, 1, "WRAM"),  # The Eye Sees All
                (0x0C02, 1, "WRAM"),  # Duck
                (0x0C2C, 1, "WRAM"),  # Claw Machine Draw (multiple items, all share this)
                (0x0CFF, 1, "WRAM"),
            ]))[0]

            # EXAMPLE: Trigger a location check if bit 3 of byte 0x02000004 is set
            if ram_data[2] >= 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010000]  # Use your actual Archipelago location ID
                }])

            received_index = ram_data[42][0]



            if ram_data[41] == 1:  # continue to check claw machine
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010038]  # Use your actual Archipelago location ID
                }])

            for i in range(len(ctx.items_received) - received_index):
               if ctx.items_received[received_index + i] .item == 2010000:
                    await bizhawk.write(ctx.bizhawk_ctx, [0x0BA6, [1], "WRAM"])
                    await bizhawk.write(ctx.bizhawk_ctx, [0x0CFF, [received_index + i + 1], "WRAM"])
                    received_index += 1

            # EXAMPLE: Send goal completion when bit 0 of byte 0x02000006 is set
            if not ctx.finished_game and (ram_data[0] == 1):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

        except bizhawk.RequestFailedError:
            # BizHawk might have lost connection—just skip this frame
            return
