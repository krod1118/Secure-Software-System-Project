# 📁 Results Directory

This folder contains all the static analysis results, visualizations, and supporting data files generated during our security assessment of Calibre’s plugin architecture.

---

## 📊 Contents

### 🗂 CSV Files
- **`bandit_results.csv`** — Exported results from Bandit’s scan of Calibre’s Python codebase. Includes file names, issue descriptions, severity levels (Low, Medium, High), and line numbers.
- **`pylint_results.csv`** — Linting results from Pylint, detailing convention issues, warnings, errors, and fatal runtime risks in plugin-related files.

### 🖼 Diagrams and Visualizations
- **`bandit_severity_chart.png`** — Bar chart showing distribution of Bandit-detected vulnerabilities by severity.
- **`pylint_pie_chart.png`** — Pie chart visualizing the proportion of Pylint code issues by type (convention, refactor, warning, error).
- **`stride_table.png`** — STRIDE threat model table showing mapped threats for the plugin system.
- **`dread_matrix.png`** — DREAD model matrix used to prioritize discovered threats based on damage potential, exploitability, and more.

---

## 🧪 Purpose

These files represent the evidence collected during our assessment and were used to:

- Identify and classify vulnerabilities
- Score threat severity
- Visualize patterns in security flaws
- Support formal threat modeling (STRIDE/DREAD)
- Back our mitigation and design recommendations
