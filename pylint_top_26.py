#!/usr/bin/env python3
import os
import sys
import pandas as pd

def main():
    INPUT_CSV = "grouped_pylint_results.csv"
    OUTPUT_CSV = "pylint_mostfound.csv"
    
    # Check input exists
    if not os.path.exists(INPUT_CSV):
        print(f"Error: '{INPUT_CSV}' not found in current directory.", file=sys.stderr)
        sys.exit(1)
    
    # Load the grouped results
    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"Error reading '{INPUT_CSV}': {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate required columns
    if "Message" not in df.columns or "Count" not in df.columns:
        print("Error: Input CSV must contain 'Message' and 'Count' columns.", file=sys.stderr)
        sys.exit(1)
    
    # Ensure Count is integer
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0).astype(int)
    
    # Sort by Count descending and take top 26
    top26 = df.sort_values("Count", ascending=False).head(26)
    
    # Write to output CSV
    try:
        top26.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Top 26 Pylint errors written to '{OUTPUT_CSV}'.")
    except Exception as e:
        print(f"Error writing '{OUTPUT_CSV}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
