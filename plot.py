import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("mid_spread.csv", index_col=0)

cols_to_plot = ["best_bid", "best_ask"]

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot best_bid and best_ask on the left y-axis
for col in cols_to_plot:
    ax1.plot(df.index, df[col], label=col, linewidth=0.5)
ax1.set_xlabel("Index")
ax1.set_ylabel("Price")
ax1.grid(True)

# Create a second y-axis for spread
ax2 = ax1.twinx()
ax2.plot(df.index, df["spread"], label="spread", color="red", linewidth=0.8)
ax2.set_ylabel("Spread", color="red")
ax2.tick_params(axis='y', labelcolor='red')

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Market without Interference")
plt.show()