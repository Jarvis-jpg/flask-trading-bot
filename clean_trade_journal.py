import json

INPUT_FILE = "trade_journal.json"
OUTPUT_FILE = "trade_journal_cleaned.json"

try:
with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
raw = f.read()

# Replace control characters and escape invalid sequences
clean_raw = raw.replace("\x00", "").replace("\x1a", "").replace("\n", "\\n")

trades = json.loads(clean_raw)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
json.dump(trades, f, indent=2)

print(f"✅ Cleaned and saved to {OUTPUT_FILE}")

except Exception as e:
print(f"❌ Error while cleaning: {e}")