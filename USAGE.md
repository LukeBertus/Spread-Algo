# Installation and Usage Guide

This guide will walk you through setting up and running the trading competition exchange simulation.

> **Need Help?** If any of these steps don't work or if you're unsure, please contact your mentor or Josh.

## Step 1: Install Miniconda

We'll use Conda to manage Python environments. This approach ensures consistent dependency management across different systems.

1. **Download Miniconda:**
   - Visit [https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)
   - Download the appropriate version for your operating system
   - **Important:** If using macOS, use the graphical installer

2. **Install Miniconda:**
   - Run the installer
   - **Critical:** Ensure you check the option to "Add conda to PATH" during installation

3. **Verify Installation:**
   - Open your terminal/command prompt
   - Type `conda` and press Enter
   - You should see conda help information (not error messages)

## Step 2: Create and Activate Virtual Environment

A virtual environment isolates your project dependencies from your system Python installation, preventing version conflicts.

1. **Create the environment:**
   ```bash
   conda create -n qfin_env python=3.12.11
   ```

2. **Activate the environment:**
   ```bash
   conda activate qfin_env
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Run the Market Simulation

Once setup is complete, you can test your trading bot!

1. **Run the simulation:**
   ```bash
   python play_game.py
   ```

2. **Expected output:**
   ```
   Random seed set to: {some number}
   Imports Completed
   You did a trade!
   ```

3. **Wait for completion:**
   - The simulation will run for a specified duration
   - Your PnL (Profit and Loss) will be displayed
   - The program will terminate automatically

## Success Indicators

✅ **Setup Complete:** If you see the expected output without errors, everything is configured correctly!

✅ **Ready to Code:** You can now modify `your_algo.py` to implement your trading strategy

✅ **Test Your Bot:** Run `play_game.py` anytime to test changes to your algorithm

## Troubleshooting

- **Conda not found:** Ensure conda was added to PATH during installation
- **Import errors:** Make sure you're in the `qfin_env` environment and dependencies are installed
- **Permission errors:** Try running terminal as administrator (Windows) or use `sudo` (macOS/Linux)

---

**Note:** Your bot currently implements a basic strategy (buys on the first timestep). This starter code allows you to verify the setup works before implementing your own trading logic.