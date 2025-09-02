import platform
import sys
import os

original_sys_path = sys.path.copy()

current_dir = os.path.dirname(os.path.abspath(__file__))
os_name = platform.system()

if os_name == "Linux":
    sys.path.insert(0, os.path.join(current_dir, "bin/linux_version"))
    from bin.linux_version.game_setup import run_game
elif os_name == "Windows":
    sys.path.insert(0, os.path.join(current_dir, "bin/windows_version"))
    from bin.windows_version.game_setup import run_game
elif os_name == "Darwin":
    sys.path.insert(0, os.path.join(current_dir, "bin/mac_version"))
    from bin.mac_version.game_setup import run_game
else:
    raise ValueError("Unsupported OS")

from base import Product

#print("Imports Completed")

sys.path = original_sys_path

# ======================Do Not Change Anything above here====================

# The following variables represent the values we will use when assessing your bot
# You may change them for testing purposes
#   (e.g. you may reduce num_timestamps when testing so that you can run simulations faster)
#   (e.g. you may set fine to 0 to see if your strategy is first profiable without position penalties)

from your_algo import PlayerAlgorithm

uec = Product("UEC", mpv=0.1, pos_limit=200, fine=20)

products = [uec]



player_bot = PlayerAlgorithm(products)
num_timestamps = 20000
0
your_pnl = run_game(player_bot, num_timestamps, products)

pnl = player_bot.positions["Cash"]

print(f"OLD: {your_pnl:.4f} NEW: {pnl:.4f}")


# Save data to csv after completion
import pandas as pd

df = pd.DataFrame(player_bot.data)
df.index.name = 'Index'
df.to_csv('mid_spread.csv')



