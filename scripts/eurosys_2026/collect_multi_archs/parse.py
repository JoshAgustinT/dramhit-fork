import re
import pandas as pd
import sys

def parse_final_log(text):
    # 1. Extract MLC Peak first to use as a baseline/reference
    mlc_match = re.search(r"Numa node\s+0\s+1\s+\n\s+0\s+(\d+\.\d+)", text)
    mlc_peak_gbs = float(mlc_match.group(1)) / 1000.0 if mlc_match else 0.0

    # 2. Find the top-level variant blocks
    variants = re.findall(r"START (\w+) \{(.*?)\} END \1", text, re.DOTALL)
    
    records = []
    
    for var_name, var_content in variants:
        # Extract Bandwidth from perf samples
        bw_pattern = r"(\d+\.\d+)\s+([\d,]+)\s+unc_m_cas_count\.(\w+)"
        bw_matches = re.findall(bw_pattern, var_content)
        
        bw_sums = {'all': [], 'rd': [], 'wr': []}
        for ts, count, event in bw_matches:
            if event in bw_sums:
                bw_sums[event].append(int(count.replace(',', '')) * 64 / 1e9)
        
        avg_bw = {k: (sum(v)/len(v) if v else 0.0) for k, v in bw_sums.items()}

        # Extract MOPS and Fill levels
        mops_sections = re.findall(r"\{.*?set_mops\s*:\s*(\d+\.\d+),\s*get_mops\s*:\s*(\d+\.\d+)\s*\}\n.*?--ht-fill (\d+)", var_content, re.DOTALL)

        for set_m, get_m, fill in mops_sections:
            records.append({
                'Variant': var_name,
                'Fill_Level': int(fill),
                'Set_MOPS': float(set_m),
                'Get_MOPS': float(get_m),
                'Total_BW': round(avg_bw['all'], 2),
                'MLC_Baseline_GBs': round(mlc_peak_gbs, 2)
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_final.py <log_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        log_text = f.read()

    df_results = parse_final_log(log_text)
    df_results.to_csv("thesis_data_with_mlc.csv", index=False)
    
    print(f"\n--- Parsed Results (MLC Peak detected: {df_results['MLC_Baseline_GBs'].iloc[0] if not df_results.empty else 0} GB/s) ---")
    print(df_results.to_string(index=False))