import subprocess
import re
from statistics import mean

def run_traceroute(host, max_hops=30):
    """Run traceroute and parse per-hop RTTs"""
    try:
        output = subprocess.run(['traceroute', '-m', str(max_hops), host], 
                              capture_output=True, text=True, timeout=60)
        return output.stdout
    except Exception as e:
        print(f"Traceroute failed for {host}: {e}")
        return None

def parse_traceroute(output):
    """Parse traceroute output, return list of (hop_num, avg_rtt)"""
    hops = []
    lines = output.split('\n')
    
    for line in lines:
        # skip header/footer
        if 'traceroute' in line or line.strip() == '':
            continue
        
        # parsing: "1  gateway (1.2.3.4)  10.5 ms  10.3 ms  10.7 ms"
        match = re.match(r'\s*(\d+)\s+', line)
        if not match:
            continue
        
        hop_num = int(match.group(1))
        
        # match "10.5 ms" patterns
        rtts = re.findall(r'(\d+\.?\d*)\s*ms', line)
        
        if rtts:
            rtt_floats = []
            for rtt in rtts:
                rtt_floats.append(float(rtt))
            avg_rtt = mean(rtt_floats)
            hops.append((hop_num, avg_rtt))
        elif '*' in line:
            # hop did not respond
            hops.append((hop_num, None))
    
    return hops

# testing outputi
if __name__ == "__main__":
	output = run_traceroute("google.com")
	if output:
	    hops = parse_traceroute(output)
	    print(hops)
