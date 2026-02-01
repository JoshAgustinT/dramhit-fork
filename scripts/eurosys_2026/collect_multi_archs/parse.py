import re
import pandas as pd
import sys

def parse_perf_output(text):
    # This regex looks for START [Name] TEST { ... } END [Name] TEST
    # It allows for extra characters (like # or whitespace) before/after the braces
    blocks = re.findall(r"START (.*?) TEST \{?\s*\n(.*?)\} END \1 TEST", text, re.DOTALL)
    
    summary = {}
    
    for test_name, content in blocks:
        data = []
        # Matches: [Timestamp] [Count] [Event Name]
        # Handles commas in counts and ignores extra text at the end of lines
        pattern = r"(\d+\.\d+)\s+([\d,]+)\s+unc_m_cas_count\.(\w+)"
        matches = re.findall(pattern, content)
        
        if not matches:
            continue
            
        for ts, count, event in matches:
            data.append({
                'time': float(ts),
                'count': int(count.replace(',', '')),
                'event': event # all, rd, wr
            })
            
        df = pd.DataFrame(data)
        
        # Pivot by time so we have 'all', 'rd', 'wr' as columns for each 1s sample
        pivot = df.pivot_table(index='time', columns='event', values='count', aggfunc='sum').fillna(0)
        
        # Bandwidth Formula: (Count * 64 bytes) / 10^9
        # Assuming 1s intervals (-I 1000 in perf)
        for col in ['all', 'rd', 'wr']:
            if col in pivot.columns:
                pivot[f'bw_{col}'] = (pivot[col] * 64) / 1e9
            else:
                pivot[f'bw_{col}'] = 0.0
        
        summary[test_name] = {
            'avg_all': pivot['bw_all'].mean(),
            'avg_rd': pivot['bw_rd'].mean(),
            'avg_wr': pivot['bw_wr'].mean()
        }
    
    return summary

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_perf.py <log_file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            log_data = f.read()
            
        results = parse_perf_output(log_data)
        
        if not results:
            print("No test blocks found. Check if your log contains 'START [Name] TEST {'")
        
        for test, stats in results.items():
            print(f"--- {test} TEST Averages ---")
            print(f"Total BW: {stats['avg_all']:8.4f} GB/s")
            print(f"Read BW:  {stats['avg_rd']:8.4f} GB/s")
            print(f"Write BW: {stats['avg_wr']:8.4f} GB/s\n")
            
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")