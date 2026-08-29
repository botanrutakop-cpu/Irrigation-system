import serial
import time
import csv
import os
from datetime import datetime

# Serial port configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Change this to your serial port
BAUD_RATE = 9600
LOG_FILE = 'irrigation_log.csv'

# CSV headers
HEADERS = ['timestamp', 'humidity', 'pump_status', 'activation_hour']

def init_csv_file():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        print(f"Created new log file: {LOG_FILE}")

def parse_arduino_data(raw_data):
    """Parse CSV data from Arduino and return as dict, or None if invalid"""
    try:
        parts = raw_data.split(',')
        if len(parts) != 3:
            print(f"WARNING: Invalid data format (expected 3 fields, got {len(parts)}): {raw_data}")
            return None
        
        humidity, pump_status, activation_hour = parts
        
        # Validate data types and convert to percentage
        raw_humidity = float(humidity.strip())
        humidity = round(((1023 - raw_humidity) / (1023 - 200)) * 100, 1)
        humidity = max(0.0, min(100.0, humidity)) # Keeps it strictly between 0-100%
        
        pump_status = pump_status.strip().lower()
        activation_hour = int(activation_hour.strip())
        
        # Validate pump status
        if pump_status not in ['on', 'off']:
            print(f"WARNING: Invalid pump status: {pump_status}")
            return None
        
        # Validate hour (0-23)
        if not (0 <= activation_hour <= 23):
            print(f"WARNING: Invalid hour (must be 0-23): {activation_hour}")
            return None
        
        return {
            'humidity': humidity,
            'pump_status': pump_status,
            'activation_hour': activation_hour
        }
    except (ValueError, IndexError) as e:
        print(f"WARNING: Could not parse data: {raw_data} ({str(e)})")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected issue parsing data: {str(e)}")
        return None

print("Starting irrigation logger...")
init_csv_file()

try: 
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for the connection to initialize
    print(f"Connected to Arduino on {SERIAL_PORT}")
    print("Waiting for data...")
    
    # Flush initial junk bytes that often flood the serial buffer on connect
    arduino.reset_input_buffer()
    
    while True:
        try:
            # Read line and decode safely using 'ignore' to prevent crashes from corrupt bytes
            raw_bytes = arduino.readline()
            raw_data = raw_bytes.decode('utf-8', errors='ignore').strip()
            
            if raw_data:
                print(f"DEBUG: Raw data received: '{raw_data}' (length: {len(raw_data)}, fields: {len(raw_data.split(','))})")
                parsed_data = parse_arduino_data(raw_data)
                
                if parsed_data:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Write to CSV
                    with open(LOG_FILE, 'a', newline='') as log_file:
                        writer = csv.writer(log_file)
                        writer.writerow([
                            timestamp,
                            parsed_data['humidity'],
                            parsed_data['pump_status'],
                            parsed_data['activation_hour']
                        ])
                    
                    # Display to console
                    print(f"{timestamp} | Humidity: {parsed_data['humidity']}% | Pump: {parsed_data['pump_status'].upper()} | Hour: {parsed_data['activation_hour']}")
        
        except UnicodeDecodeError:
            print("WARNING: Dropped corrupted serial byte data.")
            
except serial.SerialException as e:
    print("ERROR: Could not connect to Arduino!")
    print("Details: " + str(e))
    print("Please check that the Arduino is plugged in and the port is correct.")
except KeyboardInterrupt:
    print("\nStopping irrigation logger...")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Serial connection closed.")
