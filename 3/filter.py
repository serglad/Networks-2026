import ipaddress
import csv

def ip_range_to_cidrs(start_ip, end_ip):
    """Convert IP range to list of CIDR blocks"""
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    
    cidrs = []
    while start <= end:
        # Find the largest CIDR block that fits
        max_size = 32
        while max_size > 0:
            mask = 32 - max_size
            size = 1 << max_size
            if start % size == 0 and start + size - 1 <= end:
                break
            max_size -= 1
        
        cidr = f"{ipaddress.IPv4Address(start)}/{32 - max_size}"
        cidrs.append(cidr)
        start += (1 << max_size)
    
    return cidrs

def generate_nginx_geo_cidr(csv_file_path, output_file_path):
    """Generate nginx geo configuration using CIDR notation"""
    
    russian_networks = set()
    
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 4 and row[2] == 'RU':
                start_ip = str(ipaddress.IPv4Address(int(row[0])))
                end_ip = str(ipaddress.IPv4Address(int(row[1])))
                
                # Convert range to CIDR blocks
                for cidr in ip_range_to_cidrs(start_ip, end_ip):
                    russian_networks.add(cidr)
    
    print(f"Generated {len(russian_networks)} CIDR blocks")
    
    with open(output_file_path, 'w') as f:
        f.write("geo $blacklist {\n")
        f.write("    default 0;\n")
        
        for network in sorted(russian_networks, key=lambda x: ipaddress.IPv4Network(x)):
            f.write(f"    {network} 1;\n")
        
        f.write("}\n")

# Usage
generate_nginx_geo_cidr("IP2LOCATION-LITE-DB1.CSV", "nginx_geo_russia_blocklist.conf")