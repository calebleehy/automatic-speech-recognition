import csv
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Create index (optional: add settings/mappings here)
index_name = "cv-transcriptions"
es.indices.create(index=index_name, ignore=400)

# Load CSV and index rows
with open("../asr/cs-valid-dev.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        doc = {
            "filename": row["filename"],
            "text": row["text"],
            "up_votes": int(row["up_votes"]),
            "down_votes": int(row["down_votes"]),
            "age": int(row["age"]),
            "gender": row["gender"],
            "accent": row["accent"],
            "duration": float(row["duration"]),
            "generated_text": row["generated_text"]
        }
        es.index(index=index_name, id=i, document=doc)
