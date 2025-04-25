# consolidate_simple.py

import os
import sys
import re
import pandas as pd

def consolidate_bandit(input_csv: str, output_csv: str):
    if not os.path.exists(input_csv):
        print(f"ERROR: Input file '{input_csv}' not found.", file=sys.stderr)
        return
    df = pd.read_csv(input_csv)
    grouped = (
        df.groupby(["Severity Level", "Message"])
          .size()
          .reset_index(name="Count")
          .sort_values(by=["Severity Level", "Count"], ascending=[False, False])
    )
    grouped.to_csv(output_csv, index=False)
    print(f"✅ Written consolidated Bandit results to '{output_csv}'")

def simplify_pylint(msg: str) -> str:
    """
    Simplify a pylint message by stripping parentheses details
    and cutting off at the first quote (single or double).
    """
    text = str(msg).strip()
    # Strip surrounding quotes
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1].strip()
    # Remove parentheses and everything after
    text = re.split(r'\s*\(', text)[0]
    # Cut off at first single or double quote
    for delim in ("'", '"'):
        if delim in text:
            text = text.split(delim, 1)[0]
    return text.strip()

def consolidate_pylint(input_csv: str, output_csv: str):
    if not os.path.exists(input_csv):
        print(f"ERROR: Input file '{input_csv}' not found.", file=sys.stderr)
        return
    df = pd.read_csv(input_csv)
    if "Message" not in df.columns:
        print(f"ERROR: 'Message' column not found in '{input_csv}'.", file=sys.stderr)
        return
    # Simplify the Message column
    df["Message"] = df["Message"].apply(simplify_pylint)
    grouped = (
        df.groupby(["Severity Level", "Message"])
          .size()
          .reset_index(name="Count")
          .sort_values(by=["Severity Level", "Count"], ascending=[False, False])
    )
    grouped.to_csv(output_csv, index=False)
    print(f"✅ Written consolidated Pylint results to '{output_csv}'")

def main():
    consolidate_bandit("bandit_results.csv", "grouped_bandit_results.csv")
    consolidate_pylint("pylint_results.csv", "grouped_pylint_results.csv")

if __name__ == "__main__":
    main()

# To run:
# 1. Activate your venv and ensure pandas is installed: pip install pandas
# 2. Place this script alongside bandit_results.csv and pylint_results.csv
# 3. Run: python consolidate_simple.py
