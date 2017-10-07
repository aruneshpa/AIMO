from ripe.atlas.sagan import PingResult, DnsResult, TracerouteResult
from ripe.atlas.cousteau import Measurement, Probe
import pickle
import json
f = open("./dns_data_new", "rb")
try:
    unpickler = pickle.Unpickler(f)
    dns_dict = unpickler.load()
except EOFError:
    pass
final_dict = dict()
count = 1
for (domain_name, value) in dns_dict.items():
    for item in value:
        for (subdomain_name, p_list) in item.items():
            print(subdomain_name)
            for p_id in p_list.keys():
                p = Probe(id=p_id)
                c_code = p.country_code
                if c_code not in final_dict:
                    final_dict[c_code] = dict()
                if subdomain_name not in final_dict[c_code]:
                    final_dict[c_code][subdomain_name] = []
                final_dict[c_code][subdomain_name].append(p_id)
    count += 1
    if count == 2:
        break

final_file = open("./countrywise_dns.json", "w")
final_file.write(json.dumps(final_dict))
final_file.close()
f.close()
