import subprocess
import re


def get_ip(s):
    match=re.search(r"\([0-9.]+\)",s)
    return s[match.start()+1:match.end()-1]


def get_avg_rtt(s):
    match=re.search(r"/[0-9.]+/",s)
    return s[match.start()+1:match.end()-1]


def get_time(s):
    match=re.search(r"[0-9.]+ms",s)
    return s[match.start():match.end()-2]


def get_loss(s):
    match=re.search(r"[0-9.]+%",s)
    return s[match.start():match.end()-1]


domains=["google.com","yandex.ru","localhost","nsu.ru","nsunet.ru",
         "www.netflix.com","zim.gov.zw","www.gov.cn","gosuslugi.ru",
         "steampowered.com"]


with open("ping.csv","w") as output_file:
    for domain in domains:
        try:
            ping_result=subprocess.check_output(["ping",domain,"-c5"]).decode("utf-8")
            print(get_ip(ping_result),end=',',file=output_file)
            print(get_avg_rtt(ping_result),end=',',file=output_file)
            print(get_time(ping_result),end=',',file=output_file)
            print(get_loss(ping_result),file=output_file)
        except:
            print(f"{-1},{-1},{-1},{-1}",file=output_file)
            print(f"Domain {domain} unreachable")