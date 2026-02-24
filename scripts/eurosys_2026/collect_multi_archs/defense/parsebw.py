import re
import pandas as pd
import sys

def parse_final_log(text):
    # --- MLC BASELINE (may appear anywhere) ---
    mlc_match = re.search(
        r"Numa node\s+0\s+1\s+\n\s+0\s+(\d+\.\d+)",
        text
    )
    mlc_peak_gbs = float(mlc_match.group(1)) / 1000.0 if mlc_match else 0.0

    # --- VARIANT BLOCKS ---
    variants = re.findall(
        r"START (\w+) \{(.*?)\} END \1",
        text,
        re.DOTALL
    )

    records = []

    for var_name, var_content in variants:
        # --- BANDWIDTH (FIND TEST ONLY) ---
        find_block_match = re.search(
            r"START FIND TEST \{(.*?)\} END FIND TEST",
            var_content,
            re.DOTALL
        )

        avg_bw = 0.0

        if find_block_match:
            find_content = find_block_match.group(1)

            bw_matches = re.findall(
                r"[\d.]+\s+([\d,]+)\s+unc_m_cas_count\.all",
                find_content
            )

            bw_samples = [
                int(c.replace(',', '')) * 64 / 1e9
                for c in bw_matches
            ]

            # --- STEADY-STATE TRIMMING ---
            if len(bw_samples) > 25:
                steady_state = bw_samples[10:-10]
            elif len(bw_samples) > 2:
                steady_state = bw_samples[1:-1]
            else:
                steady_state = bw_samples

            if steady_state:
                avg_bw = sum(steady_state) / len(steady_state)

        # --- SINGLE UNIFORM TEST (ONE PER VARIANT) ---
        mops_match = re.search(
            r"\{\s*set_cycles.*?"
            r"set_mops\s*:\s*([\d.]+),\s*"
            r"get_mops\s*:\s*([\d.]+)\s*\}"
            r".*?--ht-fill\s+(\d+)",
            var_content,
            re.DOTALL
        )

        if mops_match:
            set_m, get_m, fill = mops_match.groups()

            records.append({
                'Variant': var_name,
                'Fill_Level': int(fill),
                'Set_MOPS': float(set_m),
                'Get_MOPS': float(get_m),
                'Total_BW_GBs': round(avg_bw, 2),
                'MLC_Baseline_GBs': round(mlc_peak_gbs, 2),
            })

    return pd.DataFrame(records)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_final.py <log_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            log_text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    df_results = parse_final_log(log_text)

    output_file = "data.csv"
    df_results.to_csv(output_file, index=False)

    if not df_results.empty:
        print("\n--- Parsed Results (Steady-State, Trimming 10/10) ---")
        print(df_results.to_string(index=False))
    else:
        print("No data found. Check FIND TEST blocks.")