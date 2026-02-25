#!/bin/python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

def plot_bandwidth_scaling(csv_file, output_file):
    # Load data
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Define identifiers and palette
    ids = df["Variant"].unique()
    # Using 'rocket' palette as requested, reversed for better contrast
    palette = sns.color_palette("rocket", n_colors=len(ids))
    palette = palette[::-1] 
    sns.set_theme(style="whitegrid")

    # Font sizes for Thesis PDF
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'pdf.fonttype': 42
    })

    fig, ax = plt.subplots(figsize=(10, 7))

    # --- Plot 1: Bandwidth Scaling (Line Plot) ---
    sns.lineplot(
        data=df, 
        x="Fill_Level", 
        y="Avg_BW_GBs", 
        hue="Variant", 
        palette=palette, 
        marker="o", 
        markersize=10, 
        linewidth=3,
        ax=ax
    )

    # --- MLC Baseline Ceiling ---
    # Get the MLC value from the first row
    mlc_val = df["MLC_Baseline_GBs"].iloc[0]
    ax.axhline(mlc_val, color='red', linestyle='--', linewidth=2.5, label="MLC Peak BW")
    
    # Label the MLC line
    ax.text(
        df["Fill_Level"].min(), 
        mlc_val + (mlc_val * 0.02), 
        f"MLC Peak: {mlc_val:.1f} GB/s", 
        color='red', 
        fontweight='bold', 
        va='bottom'
    )

    # --- Formatting ---
    ax.set_title("Memory Bandwidth Scaling vs. Table Fill Factor", pad=20)
    ax.set_xlabel("Hash Table Fill Level (%)")
    ax.set_ylabel("Sustained Bandwidth (GB/s)")
    
    # Set Y-axis to start at 0 and go slightly above MLC peak for headroom
    ax.set_ylim(0, mlc_val * 1.15)
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
    
    ax.grid(True, which="major", axis="both", linestyle="--", alpha=0.7)

    # --- Legend ---
    # Create custom legend to include the MLC Peak line
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=[l.upper() for l in labels], 
              loc='lower left', frameon=True, shadow=True)

    plt.tight_layout()
    
    # Save as PDF
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    print(f"[OK] Bandwidth plot saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plot_bw.py data.csv [output.pdf]")
        sys.exit(1)

    csv_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else "bandwidth_scaling.pdf"
    
    plot_bandwidth_scaling(csv_input, pdf_output)