from platform import system
from typing import TYPE_CHECKING
import asyncio
import logging
from NetUtils import ClientStatus

import random
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class SSClient(BizHawkClient):
    game = "Severed Soul"           # Match this with your World name
    system = "GB"                  # SNES, GBA, etc.
    patch_suffix = ".apss"    # Optional: show these files in "Open Patch"
    death_link_ready = False
    previous_death_link = 0
    tagged = -1
    hinted_claw = False
    hinted_store = False


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
                (0x0BAA, 1, "WRAM"),  # Release
                (0x0BAE, 1, "WRAM"),  # Claw Machine Interact
                (0x0BB8, 1, "WRAM"), #W1L1
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
                (0x0BDA, 1, "WRAM"), # Coin 1 W3L1
                (0x0BDC, 1, "WRAM"), # Coin 2 W3L1
                (0x0BDE, 1, "WRAM"), # Coin 3 W3L1
                (0x0BE0, 1, "WRAM"),
                (0x0BE2, 1, "WRAM"),
                (0x0BE4, 1, "WRAM"),
                (0x0BE6, 1, "WRAM"),
                (0x0BEC, 1, "WRAM"),
                (0x0BEA, 1, "WRAM"),
                (0x0BE8, 1, "WRAM"),
                (0x0BEE, 1, "WRAM"),
                (0x0BFA, 1, "WRAM"),
                (0x0BFC, 1, "WRAM"),
                (0x0BFE, 1, "WRAM"),
                (0x0C00, 1, "WRAM"),
                (0x0C02, 1, "WRAM"),
                (0x0BF0, 1, "WRAM"),
                (0x0BF2, 1, "WRAM"),
                (0x0BF4, 1, "WRAM"),
                (0x0BF6, 1, "WRAM"),
                (0x0BF8, 1, "WRAM"),
                (0x0C04, 1, "WRAM"),  # Slime-y Secret
                (0x0C06, 1, "WRAM"),  # The Eye Sees All
                (0x0C08, 1, "WRAM"),  # Duck
                (0x0C96, 1, "WRAM"),  # Claw Machine Draw (multiple items, all share this)
                (0x0CFF, 1, "WRAM"),
                (0x0B98, 1, "WRAM"), # coins maybe
                (0x0B9E, 1, "WRAM"), # Secret Checks
                (0x0B94, 1, "WRAM"), # health so it can go bye bye
                (0x0C14, 1, "WRAM"), # KK (48)
                (0x0C10, 1, "WRAM"), # Tetris
                (0x0C0A, 1, "WRAM"), # sage
                (0x0C16, 1, "WRAM"), #pits
                (0x0BB4, 1, "WRAM"), # Claw Machine Interact so I can hint it lmao (52)
                (0x0C18, 1, "WRAM"), # W1L1
                (0x0C1A, 1, "WRAM"), # W1L2
                (0x0C1C, 1, "WRAM"), # W1L3
                (0x0C1E, 1, "WRAM"), # W1L4
                (0x0C20, 1, "WRAM"), # W2L1
                (0x0C22, 1, "WRAM"), # W2L2
                (0x0C24, 1, "WRAM"), # W2L3
                (0x0C26, 1, "WRAM"), # W2L4
                (0x0C28, 1, "WRAM"), # W3L1
                (0x0C2A, 1, "WRAM"), # W3L2
                (0x0C2C, 1, "WRAM"), # W3L3
                (0x0C2E, 1, "WRAM"), # W3L4
                (0x0C30, 1, "WRAM"), # W3L5 (65)
                (0x0C32, 1, "WRAM"), # W3L6
                (0x0C34, 1, "WRAM"), #enem 1 (67)
                (0x0C36, 1, "WRAM"),
                (0x0C38, 1, "WRAM"),
                (0x0C3A, 1, "WRAM"),
                (0x0C3C, 1, "WRAM"),
                (0x0C3E, 1, "WRAM"),
                (0x0C40, 1, "WRAM"),
                (0x0C42, 1, "WRAM"),
                (0x0C44, 1, "WRAM"),
                (0x0C46, 1, "WRAM"),
                (0x0C48, 1, "WRAM"),
                (0x0C4A, 1, "WRAM"),
                (0x0C4C, 1, "WRAM"),
                (0x0C4E, 1, "WRAM"),
                (0x0C50, 1, "WRAM"),
                (0x0C52, 1, "WRAM"), # (82)
                (0x0C12, 1, "WRAM"), # 83 (sam dont you dare get up there!)
                (0x0C56, 1, "WRAM"), # 84
                (0x0C58, 1, "WRAM"), # 85 pit trapsss
                (0x0C5A, 1, "WRAM"), # Secret Shop Hints
                (0x0C5C, 1, "WRAM"), # 87 item #1 (trinket)
                (0x0C5E, 1, "WRAM"), # 88a
                (0x0C60, 1, "WRAM"), #89
                (0x0C62, 1, "WRAM"), #90
                (0x0C64, 1, "WRAM"), #91
                (0x0C66, 1, "WRAM"), #92
                (0x0C68, 1, "WRAM"), #93
                (0x0C6A, 1, "WRAM"), #94
                (0x0C70, 1, "WRAM"), #95 shop examine
            ]))


            await self.handle_death_link(ctx, ram_data[47][0])
            if self.tagged < 0:
                if ctx.slot_info is not None:
                    if ctx.slot_data.get("death_link") == 0:
                        self.tagged = 0
                        await ctx.update_death_link(False)
                    else:
                        self.tagged = 1
                        self.previous_death_link = ctx.bizhawk_ctx
                        await ctx.update_death_link(True)


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

        # level completions

            if ram_data[53][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010083]  # Use your actual Archipelago location ID
                }])

            if ram_data[54][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010084]  # Use your actual Archipelago location ID
                }])

            if ram_data[55][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010085]  # Use your actual Archipelago location ID
                }])
            if ram_data[56][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010086]  # Use your actual Archipelago location ID
                }])

            if ram_data[57][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010087]  # Use your actual Archipelago location ID
                }])

            if ram_data[58][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010088]  # Use your actual Archipelago location ID
                }])
            if ram_data[59][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010089]  # Use your actual Archipelago location ID
                }])

            if ram_data[60][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010090]  # Use your actual Archipelago location ID
                }])

            if ram_data[61][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010091]  # Use your actual Archipelago location ID
                }])
            if ram_data[62][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010092]  # Use your actual Archipelago location ID
                }])

            if ram_data[63][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010093]  # Use your actual Archipelago location ID
                }])

            if ram_data[64][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010094]  # Use your actual Archipelago location ID
                }])

            if ram_data[65][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010095]  # Use your actual Archipelago location ID
                }])

            if ram_data[66][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010096]  # Use your actual Archipelago location ID
                }])

        # secret crap or something idk

            if ram_data[42][0] == 1:  # duck
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010050]  # Use your actual Archipelago location ID
                }])

            if ram_data[83][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010082]  # Use your actual Archipelago location ID
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

            if ram_data[48][0] == 1:  # KK
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010064]  # Use your actual Archipelago location ID
                }])

            if ram_data[49][0] == 1:  # Tetris
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010063]  # Use your actual Archipelago location ID
                }])

            if ram_data[50][0] == 1:  # Sage
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010065]  # Use your actual Archipelago location ID
                }])

            #enemy hits this is going to be great

            if ram_data[67][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010066]  # Use your actual Archipelago location ID
                }])

            if ram_data[68][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010067]  # Use your actual Archipelago location ID
                }])

            if ram_data[69][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010068]  # Use your actual Archipelago location ID
                }])

            if ram_data[70][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010069]  # Use your actual Archipelago location ID
                }])

            if ram_data[71][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010070]  # Use your actual Archipelago location ID
                }])

            if ram_data[72][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010071]  # Use your actual Archipelago location ID
                }])

            if ram_data[73][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010072]  # Use your actual Archipelago location ID
                }])

            if ram_data[74][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010073]  # Use your actual Archipelago location ID
                }])

            if ram_data[75][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010074]  # Use your actual Archipelago location ID
                }])

            if ram_data[76][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010075]  # Use your actual Archipelago location ID
                }])

            if ram_data[77][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010076]  # Use your actual Archipelago location ID
                }])

            if ram_data[78][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010077]  # Use your actual Archipelago location ID
                }])

            if ram_data[79][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010078]  # Use your actual Archipelago location ID
                }])

            if ram_data[80][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010079]  # Use your actual Archipelago location ID
                }])

            if ram_data[81][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010080]  # Use your actual Archipelago location ID
                }])

            if ram_data[82][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010081]  # Use your actual Archipelago location ID
                }])

            if ram_data[84][0] == 1:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010105]  # Use your actual Archipelago location ID
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


            if ram_data[46][0] == 1:  # continue to check secrets
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010052]
                }])
            elif ram_data[46][0] == 2:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010053]
                }])
            elif ram_data[46][0] == 3:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010054]
                }])
            elif ram_data[46][0] == 4:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010055]
                }])

            if ram_data[87][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010097]}])

            if ram_data[88][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010098]}])

            if ram_data[89][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010099]}])

            if ram_data[90][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010100]}])

            if ram_data[91][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010101]}])

            if ram_data[92][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010102]}])

            if ram_data[93][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010103]}])

            if ram_data[94][0] == 1:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [2010104]}])


            if ram_data[51][0] == 1:  # pits
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010056]
                }])
            elif ram_data[51][0] == 2:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010057]
                }])
            elif ram_data[51][0] == 3:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010058]
                }])
            elif ram_data[51][0] == 4:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010059]
                }])
            elif ram_data[51][0] == 5:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010060]
                }])
            elif ram_data[51][0] == 6:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010061]
                }])
            elif ram_data[51][0] == 7:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2010062]
                }])

            if not self.hinted_claw:
                if ram_data[52][0] == 1:
                    await ctx.send_msgs([{"cmd": "LocationScouts", "locations": [2010038, 2010039, 2010040, 2010041, 2010042, 2010043, 2010044, 2010045, 2010046, 2010047], "create_as_hint": 2}])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "yay I found the claw machine. whaddya all want?"}])
                    self.hinted_claw = True

            if not self.hinted_store:
                if ram_data[86][0] == 1:
                    await ctx.send_msgs([{"cmd": "LocationScouts", "locations": [2010097, 2010098, 2010099, 2010100, 2010101, 2010102, 2010103, 2010104], "create_as_hint": 2}])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "okay, creepy old store. whaddya all want?"}])
                    self.hinted_store = True



            for i in range(len(ctx.items_received) - received_index):
                if ctx.items_received[received_index + i].item == 2010000: # W2 Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BAC, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "finally, took you long enough for that key."}])

                elif ctx.items_received[received_index + i].item == 2010001: # W3 Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BAE, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "yeeeeeesh, been waiting a looooooong time. thanks anyway"}])

                elif ctx.items_received[received_index + i].item == 2010002: # End Credits Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BB0, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "finally, I can beat this and sit back and watch again."}])

                elif ctx.items_received[received_index + i].item == 2010003: # Claw Machine Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0BB2, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "let's go gambling!!!!!!!!!!!!!!"}])

                elif ctx.items_received[received_index + i].item == 2010015: # mystery shop key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0C6C, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010004: # Coins
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B98, [min(ram_data[45][0] + 1, 255)], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "thanks. that was so useful"}])

                elif ctx.items_received[received_index + i].item == 2010014: # 10 Coins
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B98, [min(ram_data[45][0] + 10, 255)], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "actually, that was just 10 times more helpful than usual"}])

                elif ctx.items_received[received_index + i].item == 2010013: # Coins
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B98, [min(ram_data[45][0] + 2, 255)], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "only 2x more helpful, but still isn't"}])

                elif ctx.items_received[received_index + i].item == 2010005: # secret 1
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9C, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010006: # secret 2
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9C, [2], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010007: # secret 3
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9C, [3], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010008: # secret 4
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9C, [4], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2010009: # death 1
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B94, [0], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "lovely. I died. time to restart that entire level again."}])

                elif ctx.items_received[received_index + i].item == 2010011: # heal 1
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B94, [ram_data[47][0] + 1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "thank you."}])

                elif ctx.items_received[received_index + i].item == 2010012: # heal 2
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B94, [ram_data[47][0] + 2], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "thank you, but double"}])

                elif ctx.items_received[received_index + i].item == 2010010: # pits trap
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0C54, [ram_data[85][0] + 1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])
                    if ctx.slot_data.get("rude_client") == 1:
                        await ctx.send_msgs([{"cmd": "Say", "text": "great"}])




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
            if ctx.slot_data.get("progress_per_lvl") == 0:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0B96, [15], "WRAM")])

            if ctx.slot_data.get("secret_ending") == 1:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9E, [1], "WRAM")])

            if ctx.slot_data.get("hidden_secret_stuff") == 1:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9A, [1], "WRAM")])

            if ctx.slot_data.get("secret_shop") == 1:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0C58, [1], "WRAM")])


    async def handle_death_link(self, ctx: "BizHawkClientContext", ghost_health: int) -> None:

        if ctx.slot_data.get("death_link") == 1 or ctx.slot_data.get("death_link") == True:

            death_message_num = random.randrange(0, 10)

            if not self.death_link_ready:
                if ghost_health > 0:
                    self.death_link_ready = True
                    return
                return

            if self.previous_death_link != ctx.last_death_link:
                if self.death_link_ready:
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0B94, [0], "WRAM")])
                    self.death_link_ready = False
                    self.previous_death_link = ctx.last_death_link

            if ghost_health == 0:
                if death_message_num == 1:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} screwed you all over. :)")
                elif death_message_num == 2:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} fell into a pit lmao.")
                elif death_message_num == 3:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} got his soul split by Bob the Wizard.")
                elif death_message_num == 4:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} couldn't dodge a bat.")
                elif death_message_num == 5:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} wasn't determined enough.")
                elif death_message_num == 6:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} died, so now you all die!")
                elif death_message_num == 7:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} died to fall damage.")
                elif death_message_num == 8:
                    await ctx.send_death(f"Hello, again, to all {ctx.player_names[ctx.slot]}'s friends. Together, we could play some rock and roll.")
                elif death_message_num == 9:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]}. Come on, man. Just, stop dying!")
                else:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} didn't play through the game, or the game's tutorial.")
                self.previous_death_link = ctx.last_death_link
                self.death_link_ready = False
