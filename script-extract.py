#!/usr/bin/python
from time import sleep
from ripe.atlas.cousteau import  Measurement
f = open("trace_domains.txt", "r")
lines = f.readlines()
ping_list = []
dns_list = []
trace_list = []

for line in lines:
    # ping_list.append(line.strip())
    # dns_list.append(line.strip())
    trace_list.append(line.strip())

id_list = []
ff = open("./resources/temp", "r")
# for line in ff.readlines():
#     id_list.append(line.strip().split())
id_list = ff.readline().split(', ')

for i in id_list:
    try:
        m = Measurement(id=i.strip())
        if m.get_type() == 'ping':
            if m.description.split()[-1] in ping_list:
                ping_list.remove(m.description.split()[-1])
        elif m.get_type() == 'dns':
            if m.description.split()[-1] in dns_list:
                dns_list.remove(m.description.split()[-1])
        elif m.get_type() == 'traceroute':
            if m.description.split()[-1] in trace_list:
                trace_list.remove(m.description.split()[-1])
    except Exception:
        print(str(i).strip())
    sleep(1)


ping_file = open("ping_domains.txt", "w")
dns_file = open("dns_domains.txt", "w")
trace_file = open("trace_domains.txt", "w")

# for domain in ping_list:
#     ping_file.write(domain + "\n")
#
# for domain in dns_list:
#     dns_file.write(domain + "\n")

for domain in trace_list:
    trace_file.write(domain + "\n")