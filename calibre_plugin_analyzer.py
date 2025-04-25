import os
import subprocess
import json
import csv
from collections import defaultdict

CALIBRE_GIT_URL = "https://github.com/kovidgoyal/calibre.git"
LOCAL_REPO_DIR = "calibre_repo"
CSV_OUTPUT = "static_analysis_results.csv"
CSV_BANDIT = "bandit_results.csv"
CSV_PYLINT = "pylint_results.csv"

# Severity mapping
BANDIT_SEVERITY_MAP = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3
}

PYLINT_SEVERITY_MAP = {
    "fatal": 4,
    "error": 4,
    "warning": 3,
    "refactor": 2,
    "convention": 1
}


def clone_repo():
    if not os.path.exists(LOCAL_REPO_DIR):
        print(f"Cloning Calibre repo into ./{LOCAL_REPO_DIR}...")
        subprocess.run(["git", "clone", CALIBRE_GIT_URL, LOCAL_REPO_DIR])
    else:
        print("Repo already exists, skipping clone.")


def find_plugin_files(root_dir):
    plugin_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if any(keyword in content for keyword in ["plugin", "load_plugin", "plugin_download"]):
                            plugin_files.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return plugin_files


def run_bandit(file_path):
    result = subprocess.run(
        ["bandit", "-f", "json", "-q", file_path],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout).get("results", [])
    except json.JSONDecodeError:
        return []


def run_pylint(file_path):
    result = subprocess.run(
        ["pylint", file_path, "--score=no", "--output-format=json"],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def write_csv(filename, rows):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["File Name", "Severity Level", "Message"])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "File Name": row["File Name"],
                "Severity Level": row["Severity Level"],
                "Message": row["Message"]
            })


def analyze_and_export():
    clone_repo()
    plugin_files = find_plugin_files(LOCAL_REPO_DIR)
    print(f"📁 Found {len(plugin_files)} plugin-related files.\n")

    all_results = []
    bandit_results = []
    pylint_results = []

    for path in plugin_files:
        rel_path = os.path.relpath(path, LOCAL_REPO_DIR)
        print(f"🔍 Analyzing: {rel_path}")

        # Bandit analysis
        bandit_issues = run_bandit(path)
        for issue in bandit_issues:
            severity_label = issue.get("issue_severity", "LOW")
            severity = BANDIT_SEVERITY_MAP.get(severity_label.upper(), 1)
            message = issue.get("issue_text", "")
            record = {
                "File Name": rel_path,
                "Severity Level": severity,
                "Tool Used": "bandit",
                "Message": message
            }
            all_results.append(record)
            bandit_results.append(record)

        # Pylint analysis
        pylint_issues = run_pylint(path)
        for issue in pylint_issues:
            severity = PYLINT_SEVERITY_MAP.get(issue.get("type"), 1)
            message = issue.get("message", "")
            record = {
                "File Name": rel_path,
                "Severity Level": severity,
                "Tool Used": "pylint",
                "Message": message
            }
            all_results.append(record)
            pylint_results.append(record)

    # Write master combined CSV
    print(f"\n📝 Writing full results to {CSV_OUTPUT}...")
    with open(CSV_OUTPUT, mode='w', newline='', encoding='utf-8') as master_csv:
        writer = csv.DictWriter(master_csv, fieldnames=["File Name", "Severity Level", "Tool Used", "Message"])
        writer.writeheader()
        writer.writerows(all_results)

    # Write split CSVs
    print(f"📝 Writing Bandit-only results to {CSV_BANDIT}...")
    write_csv(CSV_BANDIT, bandit_results)

    print(f"📝 Writing Pylint-only results to {CSV_PYLINT}...")
    write_csv(CSV_PYLINT, pylint_results)

    print("✅ Analysis and export complete.")


if __name__ == "__main__":
    analyze_and_export()
