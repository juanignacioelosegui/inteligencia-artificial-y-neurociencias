import re
from collections import Counter

patron:str = r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'

ips:list[str] = []
with open('access.log') as f:
    for linea in f:
    	ips.extend(re.findall(patron, linea))

for ip, n in Counter(ips).most_common():
    print(f'{n:7d} {ip}')

