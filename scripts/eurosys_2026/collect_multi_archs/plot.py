#!/bin/python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

def plot_thesis_results(csv_file, output_file):
    # Load data
    df = pd.read_csv(csv_file)
    
    # 1. Matching Paper Style: Rocket Palette (reversed) and whitegrid
    ids = df["Variant"].unique()
    palette = sns.color_palette("rocket", n_colors=len(ids))
    palette = palette[::-1]  # reverse the palette
    sns.set_theme(style="whitegrid", palette=palette)

    # 2. Increase font sizes for better readability in a thesis/PDF
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12
    })

    # Create 1x3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 7))

    # --- Plot 1: Inserts (Set MOPS) ---
    ax = axes[0]
    sns.lineplot(data=df, x="Fill_Level", y="Set_MOPS", hue="Variant", 
                 marker="o", markersize=8, ax=ax, legend=False)
    ax.set_title("Set Throughput")
    ax.set_xlabel("Fill Factor (%)")
    ax.set_ylabel("Throughput (MOPS)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", axis="both", linestyle="--")

    # --- Plot 2: Bandwidth (Bar + MLC Line) ---
    ax = axes[1]
    bw_summary = df.groupby("Variant")["Total_BW"].mean().reset_index()
    mlc_val = df["MLC_Baseline_GBs"].iloc[0]

    sns.barplot(data=bw_summary, x="Variant", y="Total_BW", ax=ax, edgecolor="black", alpha=0.9)
    # Add MLC Ceiling line
    ax.axhline(mlc_val, color='red', linestyle='--', linewidth=2, label="MLC Peak")
    ax.text(0.5, mlc_val + 1, f"MLC Peak: {mlc_val:.1f} GB/s", color='red', 
            fontweight='bold', ha='center', va='bottom')
    
    ax.set_title("Memory Bandwidth Utilization")
    ax.set_ylabel("Bandwidth (GB/s)")
    ax.set_xlabel("") # Variant names on x-axis are clear
    ax.set_ylim(0, mlc_val + 15)

    # --- Plot 3: Finds (Get MOPS) ---
    ax = axes[2]
    sns.lineplot(data=df, x="Fill_Level", y="Get_MOPS", hue="Variant", 
                 marker="o", markersize=8, ax=ax, legend=False)
    ax.set_title("Find Throughput")
    ax.set_xlabel("Fill Factor (%)")
    ax.set_ylabel("Throughput (MOPS)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", axis="both", linestyle="--")

    # --- Global Legend ---
    # Legend at the top, matching paper style formatting
    custom_lines = [
        Line2D([0], [0], color=palette[i], marker="o", label=uid.upper())
        for i, uid in enumerate(ids)
    ]
    fig.legend(
        handles=custom_lines,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.95),
        ncol=len(ids),
        fontsize=14,
        frameon=False
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    
    # Save as PDF (vector format) for thesis
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    print(f"[OK] Plots saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plot_thesis.py <input.csv> <output.pdf>")
        sys.exit(1)

    csv_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else "thesis_results.pdf"
    
    plot_thesis_results(csv_input, pdf_output)