#!/usr/bin/env python
import argparse
import csv
import datetime
import glob
import json
import os
import uuid


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="CSV to info chunks")
    parser.add_argument('--input-folder', required=True, help="Input folder path for CSV files")
    parser.add_argument('--output-folder', required=True, help="Output folder path for JSON files")
    parser.add_argument('--force', action='store_true', help="Forcefully regenerate all JSON files")

    return parser.parse_args()


def csv_to_info_chunks(input_folder, output_folder, force=False):
    os.makedirs(output_folder, exist_ok=True)

    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

    for csv_file in csv_files:
        json_file = csv_file.replace(".csv", ".json")

        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                meta = json.load(f)

            existing_files = glob.glob(os.path.join(output_folder, f"doc-id_{meta['sheet_id']}_sha_*_row_*.json"))
            if not force and existing_files:
                print(f"Skipping {meta['sheet_name']} ({meta['worksheet_name']}), already processed.")
                continue

            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)

                for i, row in enumerate(reader, 1):
                    content = " ".join(row)

                    info_chunk = {
                        "id": f'{str(uuid.uuid4())}_{i}',
                        "time": datetime.datetime.utcnow().isoformat() + "Z",
                        "content": content,
                        "embeddings": [],
                        "type": "google_sheet",
                        "sheet_id": meta["sheet_id"],
                        "sheet_name": meta["sheet_name"],
                        "worksheet_name": meta["worksheet_name"],
                        "download_time": meta["download_time"],
                        "download_filepath": meta["download_filepath"],
                        "row": i
                    }
                    filename = os.path.basename(meta['download_filepath']).replace(".csv", "")
                    output_file = os.path.join(output_folder, f"{filename}_row_{i}.json")
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(info_chunk, f, indent=4, ensure_ascii=False)


def main():
    args = parse_cli_arguments()
    csv_to_info_chunks(args.input_folder, args.output_folder, args.force)


if __name__ == "__main__":
    main()
