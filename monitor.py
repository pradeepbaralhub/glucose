import time
import json
import os
from datetime import datetime
from pydexcom import Dexcom

# --- CONFIGURATION ---
USER = "baralhub@gmail.com"
PASS = "Xdexcomg6!"
# Ensure this matches your Mac folder path exactly
FOLDER_PATH = "/Users/pradeepbaral/PycharmProjects/PytestPython/glucose"
DATA_FILE = os.path.join(FOLDER_PATH, "data.json")


def start_monitoring():
    try:
        # Using named arguments to avoid the 'positional argument' error
        # Added region="us" for California accounts
        dexcom = Dexcom(username=USER, password=PASS, region="us")
        print(f"✅ Connection Established at {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"❌ Initial Connection Failed: {e}")
        return

    while True:
        try:
            reading = dexcom.get_current_glucose_reading()

            if reading:
                # 1. Prepare the new entry
                new_entry = {
                    "value": str(reading.value),
                    "trend": reading.trend_description,
                    "time": reading.datetime.strftime("%a, %b %d, %Y %I:%M %p")
                }

                # 2. Manage the Ledger (List)
                history = []
                if os.path.exists(DATA_FILE):
                    try:
                        with open(DATA_FILE, 'r') as f:
                            history = json.load(f)
                            # Ensure we are working with a list
                            if not isinstance(history, list):
                                history = []
                    except:
                        history = []

                # 3. Add newest reading to the TOP
                history.insert(0, new_entry)

                # 4. Limit to last 10 entries for the fridge display
                history = history[:10]

                # 5. Save the entire list back to data.json
                with open(DATA_FILE, 'w') as f:
                    json.dump(history, f)

                print(f"📊 [{new_entry['time']}] Glucose: {new_entry['value']} mg/dL | {new_entry['trend']}")
            else:
                print("⏳ Waiting for new sensor data (Updates every 5 mins)...")

            # Sleep for 5 minutes
            time.sleep(300)

        except Exception as e:
            print(f"⚠️ Sync Error: {e}")
            # If session expires, try to re-initialize
            try:
                dexcom = Dexcom(username=USER, password=PASS, region="us")
            except:
                pass
            time.sleep(60)


if __name__ == "__main__":
    start_monitoring()