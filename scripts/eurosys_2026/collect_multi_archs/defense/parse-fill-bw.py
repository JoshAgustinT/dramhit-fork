import re
import pandas as pd
import sys

def parse_final_log(text):
    # 1. MLC Peak Baseline
    mlc_match = re.search(r"0\s+(\d+\.\d+)\s+\d+\.\d+", text)
    mlc_peak_gbs = float(mlc_match.group(1)) / 1000.0 if mlc_match else 0.0

    # 2. Extract Variant Blocks (dramhit23, folklore, etc.)
    variant_blocks = re.findall(r"START (\w+) \{(.*?)\} END \1", text, re.DOTALL)
    
    records = []
    # The implied sequence from your shell script loop: 10 to 90
    FILL_LEVELS = [10, 20, 30, 40, 50, 60, 70, 80, 90]

    for var_name, var_content in variant_blocks:
        # 3. Find all FIND TEST blocks within this variant
        find_blocks = re.findall(r"START FIND TEST \{(.*?)\} END FIND TEST", var_content, re.DOTALL)

        for i, block_content in enumerate(find_blocks):
            # Extract CAS counts (unc_m_cas_count.all)
            bw_matches = re.findall(r"[\d.]+\s+([\d,]+)\s+unc_m_cas_count\.all", block_content)
            
            if not bw_matches:
                continue

            # Convert to GB/s (Count * 64 bytes / 1e9)
            bw_samples = [int(c.replace(',', '')) * 64 / 1e9 for c in bw_matches]

            # --- STEADY-STATE TRIMMING (Ignore first 10, last 10) ---
            if len(bw_samples) > 25:
                steady_state = bw_samples[10:-10]
            elif len(bw_samples) > 2:
                steady_state = bw_samples[1:-1]
            else:
                steady_state = bw_samples

            avg_bw = sum(steady_state) / len(steady_state) if steady_state else 0.0
            
            # Map the iteration index to the implied fill level
            fill_val = FILL_LEVELS[i] if i < len(FILL_LEVELS) else f"Extra_{i}"

            records.append({
                'Variant': var_name,
                'Fill_Level': fill_val,
                'Avg_BW_GBs': round(avg_bw, 3),
                'MLC_Baseline_GBs': round(mlc_peak_gbs, 2),
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parsebw.py <log_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            log_text = f.read()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    df = parse_final_log(log_text)
    
    if not df.empty:
        # Save to data.csv as requested
        df.to_csv("data.csv", index=False)
        print("\n--- Results saved to data.csv ---")
        print(df.to_string(index=False))
    else:
        print("No data found. Check if perf output is correctly nested in the log.")