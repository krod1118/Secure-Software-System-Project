import csv

def sort_csv(input_path):
    with open(input_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Convert severity to int and sort descending
    rows.sort(key=lambda row: int(row["Severity Level"]), reverse=True)

    with open(input_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["File Name", "Severity Level", "Message"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Sorted by severity: {input_path}")


def main():
    sort_csv("bandit_results.csv")
    sort_csv("pylint_results.csv")


if __name__ == "__main__":
    main()
