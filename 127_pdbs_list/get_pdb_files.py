#!/usr/bin/env python3

import os
import requests
import argparse

def download_pdb(pdb_id, output_dir):
    """
    Download a PDB file given its ID and save it to the specified directory.
    :param pdb_id: The PDB ID (e.g., "3O0V")
    :param output_dir: The directory to save the downloaded PDB file
    """
    base_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    output_file = os.path.join(output_dir, f"{pdb_id}.pdb")
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {pdb_id}.pdb")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {pdb_id}.pdb: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download PDB files from a TSV file containing PDB IDs.")
    parser.add_argument("tsv_file", help="The TSV file containing PDB IDs.")
    parser.add_argument("-o", "--output_dir", default="pdb_files", help="The directory to save downloaded PDB files.")
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Read PDB IDs from the TSV file
    with open(args.tsv_file, "r") as file:
        content = file.read().strip()
        pdb_ids = content.split('\t')

    print(f"Found {len(pdb_ids)} PDB IDs. Starting download...")
    
    for pdb_id in pdb_ids:
        download_pdb(pdb_id, args.output_dir)

    print("All downloads complete.")

if __name__ == "__main__":
    main()
