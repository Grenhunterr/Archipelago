from platform import system
from typing import TYPE_CHECKING
from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.AutoWorld import World

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
            ctx.game = self.game
            ctx.items_handling = 0b011  # Server sends items
            ctx.want_slot_data = True
            return True
        except bizhawk.RequestFailedError:
            return False  # Can't confirm ROM, deny

        # ROM is valid


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

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
                (0x0BD4, 1, "WRAM"), # Coin 1 W3L1
                (0x0BD6, 1, "WRAM"), # Coin 2 W3L1
                (0x0BD8, 1, "WRAM"), # Coin 3 W3L1
                (0x0BDA, 1, "WRAM"),
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
                (0x0B98, 1, "WRAM"), #coins maybe
            ]))
            print(ram_data)
            print(len(ram_data))



            # EXAMPLE: Trigger a location check if bit 3 of byte 0x02000004 is set
            if ram_data[2][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010000]  # Use your actual Archipelago location ID
                }])

            if ram_data[3][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010001]  # Use your actual Archipelago location ID
                }])

            if ram_data[4][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010002]  # Use your actual Archipelago location ID
                }])

            if ram_data[5][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010003]  # Use your actual Archipelago location ID
                }])

            if ram_data[6][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010004]  # Use your actual Archipelago location ID
                }])

            if ram_data[7][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010005]  # Use your actual Archipelago location ID
                }])

            if ram_data[8][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010006]  # Use your actual Archipelago location ID
                }])

            if ram_data[9][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010007]  # Use your actual Archipelago location ID
                }])

            if ram_data[10][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010008]  # Use your actual Archipelago location ID
                }])

            if ram_data[11][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010009]  # Use your actual Archipelago location ID
                }])

            if ram_data[12][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010010]  # Use your actual Archipelago location ID
                }])

            if ram_data[13][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010011]  # Use your actual Archipelago location ID
                }])

            if ram_data[14][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010012]  # Use your actual Archipelago location ID
                }])

            if ram_data[15][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010013]  # Use your actual Archipelago location ID
                }])

            if ram_data[16][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010014]  # Use your actual Archipelago location ID
                }])

            if ram_data[17][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010015]  # Use your actual Archipelago location ID
                }])

            if ram_data[18][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010016]  # Use your actual Archipelago location ID
                }])

            if ram_data[19][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010017]  # Use your actual Archipelago location ID
                }])

            if ram_data[20][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010018]  # Use your actual Archipelago location ID
                }])

            if ram_data[21][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010019]  # Use your actual Archipelago location ID
                }])

            if ram_data[22][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010020]  # Use your actual Archipelago location ID
                }])

            if ram_data[23][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010021]  # Use your actual Archipelago location ID
                }])

            if ram_data[24][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010022]  # Use your actual Archipelago location ID
                }])

            if ram_data[25][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010023]  # Use your actual Archipelago location ID
                }])

            if ram_data[26][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010024]  # Use your actual Archipelago location ID
                }])

            if ram_data[27][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010025]  # Use your actual Archipelago location ID
                }])

            if ram_data[28][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010026]  # Use your actual Archipelago location ID
                }])

            if ram_data[29][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010027]  # Use your actual Archipelago location ID
                }])

            if ram_data[30][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010028]  # Use your actual Archipelago location ID
                }])

            if ram_data[31][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010029]  # Use your actual Archipelago location ID
                }])

            if ram_data[32][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010030]  # Use your actual Archipelago location ID
                }])

            if ram_data[33][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010031]  # Use your actual Archipelago location ID
                }])

            if ram_data[34][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010032]  # Use your actual Archipelago location ID
                }])

            if ram_data[35][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010033]  # Use your actual Archipelago location ID
                }])

            if ram_data[36][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010034]  # Use your actual Archipelago location ID
                }])

            if ram_data[37][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010035]  # Use your actual Archipelago location ID
                }])

            if ram_data[38][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010036]  # Use your actual Archipelago location ID
                }])

            if ram_data[39][0] == 1:  # check coin
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010037]  # Use your actual Archipelago location ID
                }])




        # secret shit or something idk

            if ram_data[42][0] == 1:  # duck
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010050]  # Use your actual Archipelago location ID
                }])

            if ram_data[41][0] == 1:  # eye
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010048]  # Use your actual Archipelago location ID
                }])

            if ram_data[40][0] == 1:  # slime
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010049]  # Use your actual Archipelago location ID
                }])







            received_index = ram_data[44][0]

            if ram_data[43][0] == 1:  # continue to check claw machine
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010038]
                }])
            elif ram_data[43][0] == 2:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010039]
                }])
            elif ram_data[43][0] == 3:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010040]
                }])
            elif ram_data[43][0] == 4:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010041]
                }])
            elif ram_data[43][0] == 5:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010042]
                }])
            elif ram_data[43][0] == 6:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010043]
                }])
            elif ram_data[43][0] == 7:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010044]
                }])
            elif ram_data[43][0] == 8:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010045]
                }])
            elif ram_data[43][0] == 9:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010046]
                }])
            elif ram_data[43][0] == 10:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010047]
                }])



            for i in range(len(ctx.items_received) - received_index):
                if ctx.items_received[received_index + i].item == 2010000: # W2 Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BA6, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010001: # W3 Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BA8, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010002: # End Credits Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BAA, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010003: # Claw Machine Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BAC, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010004: # Coins
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B98, [min(ram_data[45][0] + 1, 255)], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])



            # EXAMPLE: Send goal completion when bit 0 of byte 0x02000006 is set
            if not ctx.finished_game and (ram_data[0][0] == 1):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True





        except bizhawk.RequestFailedError:
            # BizHawk might have lost connection—just skip this frame
            return

        if ctx.slot_info is not None:
            print(ctx.slot_data)
            print(ctx.slot_info)
            if ctx.slot_data.get("progress_per_lvl") == 1:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0B96, [15], "WRAM")])