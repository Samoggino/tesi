import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to the CSV file (modify if needed)
csv_file = "data.csv"

# Read the CSV file
df = pd.read_csv(csv_file)

# Convert 'Snapshot' column to integer (represents the year)
df["Snapshot"] = df["Snapshot"].astype(int)

important_metrics = ["Clustering", "APL", "Avg Neighbors", "Centralization", "σ", "CC"]

# Convert metrics to float, handling comma as decimal separator
for col in important_metrics:
    df[col] = df[col].apply(lambda x: float(str(x).replace(",", ".")))

# Define the order of categories for the x-axis
category_order = [
    "unfiltered",
    "min_2",
    "top10 excluded & min_2",
    "top100 excluded & min_2",
]

# Mapping for simplified legend labels
category_labels = {
    "unfiltered": "unfiltered",
    "min_2": "channels >= 2",
    "top10 excluded & min_2": "top10 removed",
    "top100 excluded & min_2": "top100 removed",
}

# Create a numeric array for categories (0, 1, 2, 3)
x_positions = np.arange(len(category_order))

# Get sorted years (from 2019 to 2025)
sorted_years = sorted(df["Snapshot"].unique())
n_years = len(sorted_years)

# Offset factor for horizontal displacement (adjust to increase/decrease separation)
offset_factor = 0.0


# Function to plot metrics by category (grouped by year)
def plot_metric(metric, ylabel, title, use_log=False):
    plt.figure(figsize=(8, 5))
    for i, year in enumerate(sorted_years):
        # Compute horizontal offset for each year (centered distribution)
        offset = (i - (n_years - 1) / 2) * offset_factor
        # Filter data for the current year and sort categories
        df_year = df[df["Snapshot"] == year].copy()
        df_year["Categoria"] = pd.Categorical(
            df_year["Categoria"], categories=category_order, ordered=True
        )
        df_year = df_year.sort_values("Categoria")
        # Compute x values with offset
        x_vals = x_positions + offset
        plt.plot(
            x_vals, df_year[metric].values, marker="o", linestyle="-", label=str(year)
        )
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x_positions, ["unfiltered", "min2", "top10", "top100"])
    if use_log:
        plt.yscale("log")
    plt.legend(title="Year")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Function to plot metric trends over time (grouped by category)


def plot_metric_by_year(metric, ylabel, title, use_log=False):
    plt.figure(figsize=(8, 5))
    for category in category_order:
        df_cat = df[df["Categoria"] == category]
        df_cat = df_cat.sort_values("Snapshot")
        label = category_labels.get(category, category)
        plt.plot(
            df_cat["Snapshot"], df_cat[metric], marker="o", linestyle="-", label=label
        )
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.title(title)
    if use_log:
        plt.yscale("log")
    plt.xticks(sorted_years)
    plt.legend(title="Category")
    plt.grid(True)
    plt.tight_layout()
    # Save the figure
    filename = f"plot/{metric}_over_time.png"
    plt.savefig(filename, dpi=300)
    plt.close()


# Create plots for each metric
# Add use_log=True to use a logarithmic scale for the y-axis
# plot_metric("Clustering", "CC", "Clustering Coefficient (CC)")
# plot_metric("APL", "APL", "Average Path Length (APL)")
# plot_metric("Avg Neighbors", "AND", "Average Neighbors Degree (AND)")
# plot_metric("Centralization", "NC", "Network Centralization (NC)")
# plot_metric("σ", "σ", "Sigma σ")
# plot_metric("CC", "Connected Components", "Connected Components")

plot_metric_by_year("Clustering", "CC", "Clustering Coefficient (CC) over time by category")
plot_metric_by_year("APL", "APL", "Average Path Length (APL) over time by category")
plot_metric_by_year("Avg Neighbors", "AND", "Average Neighbors Degree (AND) over time by category")
plot_metric_by_year("Centralization", "NC", "Network Centralization (NC) over time by category")
plot_metric_by_year("σ", "σ", "Sigma σ over time by category")
plot_metric_by_year("CC", "Connected Components", "Connected Components over time by category")



# Optional: plot metrics over time for only the 'unfiltered' category
# def plot_metric_unfiltered(metric, ylabel, title, use_log=False):
#     plt.figure(figsize=(8, 5))
#     df_unfiltered = df[df["Categoria"] == "unfiltered"]
#     plt.plot(
#         sorted_years,
#         df_unfiltered.groupby("Snapshot")[metric].mean(),
#         marker="o",
#         linestyle="-",
#         label=metric
#     )
#     plt.xlabel("Year")
#     plt.ylabel(ylabel)
#     plt.title(title)
#     if use_log:
#         plt.yscale("log")
#     plt.grid(True)
#     plt.xticks(sorted_years)
#     plt.show()

# # Generate time trend plots for each metric (unfiltered only)
# plot_metric_unfiltered("Clustering", "CC", "Clustering Coefficient (CC) over time")
# plot_metric_unfiltered("APL", "APL", "Average Path Length (APL) over time")
# plot_metric_unfiltered("Avg Neighbors", "AND", "Average Neighbors Degree (AND) over time")
# plot_metric_unfiltered("Centralization", "NC", "Network Centralization (NC) over time")
# plot_metric_unfiltered("σ", "σ", "Sigma σ over time")
# plot_metric_unfiltered("CC", "Connected Components", "Connected Components over time")
