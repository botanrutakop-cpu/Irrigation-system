# Irrigation-system
a small project i made for fun and experience  :)
# This is my first IoT project: Smart Irrigation Logger

This is officially my **very first project combining coding and electronics**! I built a **Python** script that communicates with an **Arduino** via USB to read, calculate, and save live soil moisture data.

## What This Project Does
* **Reads Arduino Data:** Creates a live connection to receive data coming straight from the sensors.
* **Smart Percentage Conversion:** Converts raw sensor numbers (0-1023) into clean, easy-to-read moisture percentages (0% - 100%).
* **Data Logging:** Automatically creates a file named `irrigation_log.csv` and appends the exact timestamp, soil moisture, and pump status.
* **Crash Protection:** Included safety error-handling so the script doesn't stop or break if the Arduino sends corrupted text or gets unplugged.

## Tech Used
* **Language:** Python 3
* **Libraries:** `pyserial` (to communicate with the hardware) along with native modules `csv`, `os`, and `datetime`.
* **Hardware:** Arduino, a soil moisture sensor, and a relay module for the pump switch. (of course with a battery pack because you dont want to risk frying everything with the USB voltage, and with                                                                                           male-male connectors, female-male connectors.)

## How To Run It
1. Clone or download this project to your computer.
2. Install the required serial package by opening your terminal and typing:
   ```bash
   pip install -r requirements.txt (pyserial>=3.5)
   ```
3. Connect your Arduino to your computer via USB (make sure the path on line 8 of `irrigation_logger.py` matches your port, like `/dev/ttyUSB0` or `COM3`).
4. Start the logger script:
   ```bash
   python3 irrigation_logger.py
   ```
