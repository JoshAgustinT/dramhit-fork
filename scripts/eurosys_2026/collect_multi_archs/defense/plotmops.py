#!/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_mops_only(csv_file, output_file):
    df = pd.read_csv(csv_file)

    # ======================================
    # ONLY EDIT THESE TWO STRUCTURES
    # ======================================
    VARIANT_LABELS = {
        "dramblast": "+Refactor",
        "dramhit23": "DramHit",
        "folklore": "Folklore",
        "dramblast_no_inline": "+2Prefetch",
        "dramblast_no_double": "+Simd",
        "dramblast_no_simd": "Baseline",
    }

    SHOW_VARIANTS = [
        "dramblast",
        "dramhit23",
        "folklore",
        "dramblast_no_inline",
        "dramblast_no_double",
        "dramblast_no_simd",
    ]

    # ======================================
    # Data prep
    # ======================================
    df = df[df["Variant"].isin(SHOW_VARIANTS)]
    df["Variant_Label"] = df["Variant"].map(VARIANT_LABELS)

    mops_df = (
        df.set_index("Variant")
          .loc[SHOW_VARIANTS]
          .reset_index()
    )

    # ======================================
    # Styling
    # ======================================
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'pdf.fonttype': 42
    })

    palette = sns.color_palette("rocket", n_colors=len(SHOW_VARIANTS))

    # ======================================
    # Plot
    # ======================================
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=mops_df,
        x="Variant_Label",
        y="Get_MOPS",
        palette=palette,
        edgecolor="black",
        alpha=0.9,
        ax=ax
    )

    ax.set_title(r"Get Throughput (70% Fill, Find Workload)")
    ax.set_ylabel("Get Throughput (MOPS)")
    ax.set_xlabel("")

    plt.tight_layout()
    plt.savefig(output_file, format="pdf", bbox_inches="tight")
    print(f"[OK] Saved plot to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 plot_mops.py <input.csv> [output.pdf]")
        sys.exit(1)

    csv_input = sys.argv[1]
    pdf_output = sys.argv[2] if len(sys.argv) > 2 else "get_mops.pdf"

    plot_mops_only(csv_input, pdf_output)