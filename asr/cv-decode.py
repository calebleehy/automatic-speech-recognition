import os
import csv
import requests
from tqdm import tqdm

INPUT_DIR = "C:/Users/caleb/cv-valid-dev"
INPUT_CSV = "C:/Users/caleb/cv-valid-dev.csv"
OUTPUT_CSV = "asr/cv-valid-dev.csv"
API_URL = "http://localhost:8001/asr"

# Collect all mp3 files
mp3_files = set(f for f in os.listdir(INPUT_DIR) if f.endswith(".mp3"))

# Read original data
rows = []
with open(INPUT_CSV, mode="r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile, delimiter=',')
    fieldnames = reader.fieldnames + ["generated_text"]
    for row in reader:
        rows.append(row)

# Transcribe and write with new column
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in tqdm(rows, desc="Transcribing"):
        mp3_filename = row.get("path") or row.get("filename")
        basename = os.path.basename(mp3_filename)
        if not basename or basename not in mp3_files:
            row["generated_text"] = "[MISSING MP3]"
            writer.writerow(row)
            continue

        filepath = os.path.join(INPUT_DIR, basename)

        try:
            with open(filepath, "rb") as f:
                response = requests.post(API_URL, files={"file": f})
            if response.status_code == 200:
                row["generated_text"] = response.json().get("transcription", "")
            else:
                row["generated_text"] = f"[ERROR {response.status_code}] {response.text}"
        except Exception as e:
            row["generated_text"] = f"[EXCEPTION] {str(e)}"

        writer.writerow(row)
