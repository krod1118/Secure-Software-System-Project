import pandas as pd 
import matplotlib.pyplot as plt

# Load results
bandit_df = pd.read_csv("bandit_severity_results.csv")
pylint_df = pd.read_csv("pylint_results.csv")

# Combine severity distributions
def plot_severity_distribution(df, tool_name):
    severity_counts = df["Severity Level"].value_counts().sort_index(ascending=False)
    labels = [f"Level {lvl}" for lvl in severity_counts.index]
    
    # Bar Chart
    plt.figure(figsize=(6, 4))
    severity_counts.plot(kind='bar', color='red' if tool_name == 'Bandit' else 'blue')
    plt.title(f"{tool_name} - Severity Distribution")
    plt.ylabel("Count")
    plt.xlabel("Severity Level (3=High, 1=Low)")
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=0)
    plt.tight_layout()
    plt.savefig(f"{tool_name.lower()}_severity_bar.png")
    plt.close()

    # Pie Chart
    plt.figure(figsize=(5, 5))
    severity_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title(f"{tool_name} - Severity Distribution (Pie)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{tool_name.lower()}_severity_pie.png")
    plt.close()

# Generate charts

plot_severity_distribution(bandit_df, "Bandit")
plot_severity_distribution(pylint_df, "Pylint")
