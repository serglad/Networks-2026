import csv
import socket
import subprocess
import platform
import re

def get_ip(domain):
    try:
        return socket.gethostbyname(domain.strip())
    except socket.gaierror:
        return None

def traceroute(ip):
    try:
        cmd = ['tracert', '-d', '-h', '15', ip] if platform.system() == 'Windows' else ['traceroute', '-n', '-m', '15', ip]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+', result.stdout)
        return ips if ips else []
    except:
        return []

def process_domains(domains, output_file='results.csv'):
    """Применить traceroute и вывести результаты в csv файл"""
    results = []
    
    for domain in domains:
        ip = get_ip(domain)
        route = traceroute(ip) if ip else []
        results.append([domain, ip or 'FAILED', ' -> '.join(route) if route else 'No route'])
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Domain', 'IP Address', 'Trace Route'])
        writer.writerows(results)
    
    print(f"Results saved to {output_file}")

domains = ['google.com', 'github.com', 'stackoverflow.com']
process_domains(domains)