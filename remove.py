import json
import glob

files = glob.glob("data*/Streaming_History_Audio_*.json")

for filename in files:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for record in data:
        record.pop("ip_addr", None)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Cleaned: {filename}")

print("DONE!")