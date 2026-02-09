import re
import pandas as pd
import sys

def parse_final_log(text):
    # 1. Extract MLC Peak (Baseline)
    mlc_match = re.search(r"Numa node\s+0\s+1\s+\n\s+0\s+(\d+\.\d+)", text)
    mlc_peak_gbs = float(mlc_match.group(1)) / 1000.0 if mlc_match else 0.0

    # 2. Split into major variant blocks
    variants = re.findall(r"START (\w+) \{(.*?)\} END \1", text, re.DOTALL)
    
    records = []
    
    for var_name, var_content in variants:
        # --- BANDWIDTH SCOPING ---
        find_block_match = re.search(r"START FIND TEST \{(.*?)\} END FIND TEST", var_content, re.DOTALL)
        
        if find_block_match:
            find_content = find_block_match.group(1)
            bw_matches = re.findall(r"[\d.]+\s+([\d,]+)\s+unc_m_cas_count\.all", find_content)
            
            # Convert counts to GB/s
            bw_samples = [int(c.replace(',', '')) * 64 / 1e9 for c in bw_matches]
            
            # --- STEADY STATE TRIMMING ---
            # We remove the first 10 and last 10 samples to ignore ramp-up/ramp-down
            if len(bw_samples) > 25: # Ensure we have enough data to actually trim
                steady_state_samples = bw_samples[10:-10]
            elif len(bw_samples) > 2:
                # If the test was short, just trim the first and last 1 sample
                steady_state_samples = bw_samples[1:-1]
            else:
                steady_state_samples = bw_samples
            
            avg_bw = sum(steady_state_samples) / len(steady_state_samples) if steady_state_samples else 0.0
        else:
            avg_bw = 0.0

        # --- MOPS & FILL LEVEL EXTRACTION ---
        mops_pattern = r"\{.*?set_mops\s*:\s*(\d+\.\d+),\s*get_mops\s*:\s*(\d+\.\d+)\s*\}\n.*?--ht-fill (\d+)"
        mops_sections = re.findall(mops_pattern, var_content, re.DOTALL)

        for set_m, get_m, fill in mops_sections:
            records.append({
                'Variant': var_name,
                'Fill_Level': int(fill),
                'Set_MOPS': float(set_m),
                'Get_MOPS': float(get_m),
                'Total_BW_GBs': round(avg_bw, 2),
                'MLC_Baseline_GBs': round(mlc_peak_gbs, 2)
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
    
    output_file = "thesis_data_steady_state.csv"
    df_results.to_csv(output_file, index=False)
    
    if not df_results.empty:
        print(f"\n--- Parsed Results (Steady-State, Trimming 10/10) ---")
        print(df_results.to_string(index=False))
    else:
        print("No data found. Check if the 'FIND TEST' blocks contain enough 1s samples.")