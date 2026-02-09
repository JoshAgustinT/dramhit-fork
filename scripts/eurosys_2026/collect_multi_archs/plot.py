#!/bin/python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

def plot_thesis_results(csv_file, output_file):
    # Load data
    df = pd.read_csv(csv_file)
    
    # Define identifiers from the 'Variant' column
    ids = df["Variant"].unique()
    
    # 1. Style: Rocket Palette (reversed) and whitegrid
    palette = sns.color_palette("rocket", n_colors=len(ids))
    palette = palette[::-1] 
    sns.set_theme(style="whitegrid")

    # 2. Font sizes for Thesis PDF
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'pdf.fonttype': 42  # Ensures text is editable in Illustrator/Acrobat
    })

    # Create 1x3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # --- Plot 1: Inserts (Set_MOPS) ---
    ax = axes[0]
    sns.lineplot(data=df, x="Fill_Level", y="Set_MOPS", hue="Variant", 
                 palette=palette, marker="o", markersize=8, ax=ax, legend=False)
    ax.set_title("Set Throughput")
    ax.set_xlabel("Fill Factor (%)")
    ax.set_ylabel("Throughput (MOPS)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", axis="both", linestyle="--")

    # --- Plot 2: Bandwidth (Bar + MLC Line) ---
    ax = axes[1]
    # Header update: Total_BW -> Total_BW_GBs
    bw_summary = df.groupby("Variant")["Total_BW_GBs"].mean().reset_index()
    mlc_val = df["MLC_Baseline_GBs"].iloc[0]

    sns.barplot(data=bw_summary, x="Variant", y="Total_BW_GBs", ax=ax, 
                palette=palette, edgecolor="black", alpha=0.9)
    
    # Add MLC Ceiling line
    ax.axhline(mlc_val, color='red', linestyle='--', linewidth=2, label="MLC Peak")
    ax.text(-0.4, mlc_val + 2, f"MLC Peak: {mlc_val:.1f} GB/s", color='red', 
            fontweight='bold', ha='left', va='bottom')
    
    ax.set_title("Avg. Memory Bandwidth")
    ax.set_ylabel("Bandwidth (GB/s)")
    ax.set_xlabel("") 
    ax.set_ylim(0, mlc_val + 40) # Extra headroom for the label

    # --- Plot 3: Finds (Get_MOPS) ---
    ax = axes[2]
    sns.lineplot(data=df, x="Fill_Level", y="Get_MOPS", hue="Variant", 
                 palette=palette, marker="o", markersize=8, ax=ax, legend=False)
    ax.set_title("Find Throughput")
    ax.set_xlabel("Fill Factor (%)")
    ax.set_ylabel("Throughput (MOPS)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", axis="both", linestyle="--")

    # --- Global Legend ---
    custom_lines = [
        Line2D([0], [0], color=palette[i], marker="o", linestyle='-', 
               lw=2, markersize=10, label=uid.upper())
        for i, uid in enumerate(ids)
    ]
    
    fig.legend(
        handles=custom_lines,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=len(ids),
        fontsize=14,
        frameon=False
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save as PDF
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    print(f"[OK] Plots saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plot_thesis.py <input.csv> [output.pdf]")
        sys.exit(1)

    csv_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else "thesis_results.pdf"
    
    plot_thesis_results(csv_input, pdf_output)