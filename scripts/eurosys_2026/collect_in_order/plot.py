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
    # Using unique variants for the legend and color mapping
    variants = df["Variant"].unique()
    palette = sns.color_palette("rocket", n_colors=len(variants))
    palette = palette[::-1]  # darker colors for the better-performing variants
    sns.set_theme(style="whitegrid")

    # 2. Optimized font sizes for thesis inclusion
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 18,
        'axes.labelsize': 15,
        'xtick.labelsize': 13,
        'ytick.labelsize': 13,
        'legend.fontsize': 14,
        'font.family': 'serif' # Common for academic papers
    })

    # Create 1x2 subplots (removed the bandwidth middle plot)
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # --- Plot 1: Set Throughput ---
    ax = axes[0]
    sns.lineplot(data=df, x="Fill_Level", y="Set_MOPS", hue="Variant", 
                 palette=palette, marker="o", markersize=9, ax=ax, legend=False)
    ax.set_title("Set Throughput")
    ax.set_xlabel("Fill Factor (%)")
    ax.set_ylabel("Throughput (MOPS)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", axis="both", linestyle="--")

    # --- Plot 2: Find Throughput ---
    ax = axes[1]
    sns.lineplot(data=df, x="Fill_Level", y="Get_MOPS", hue="Variant", 
                 palette=palette, marker="s", markersize=9, ax=ax, legend=False)
    ax.set_title("Find Throughput")
    ax.set_xlabel("Fill Factor (%)")
    ax.set_ylabel("Throughput (MOPS)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", axis="both", linestyle="--")

    # --- Global Legend ---
    # Centered above the plots
    custom_lines = [
        Line2D([0], [0], color=palette[i], lw=2, marker='o' if i%2==0 else 's', 
               label=v.replace('_', ' ').upper())
        for i, v in enumerate(variants)
    ]
    
    fig.legend(
        handles=custom_lines,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.98),
        ncol=2, # Two rows of two for better spacing
        frameon=True,
        edgecolor='0.8'
    )

    # Adjust layout to make room for the legend at the top
    plt.tight_layout(rect=[0, 0, 1, 0.88])
    
    # Save as PDF (vector format) for perfect scaling in LaTeX/Thesis
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    print(f"[OK] Plots saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plot_thesis.py <input.csv> <output.pdf>")
        sys.exit(1)

    csv_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else "throughput_results.pdf"
    
    plot_thesis_results(csv_input, pdf_output)