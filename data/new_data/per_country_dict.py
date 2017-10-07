from json import dumps, load, loads
f_list = ['countrywise_dns.json', 'countrywise_ping.json', 'countrywise_trace.json']
for f_index in f_list:
    f = open(f_index, 'r')
    data_dict = load(f)
    f.close()
final_dict = dict()
for (country_code, values) in data_dict.items():
    probe_set = set()
    for (subdomain, probe_list) in values.items():
        if not probe_set or len(probe_set) == 0:
            probe_set = set(probe_list)
        else:
            probe_set = probe_set.intersection(set(probe_list))
    final_dict[country_code] = list(probe_set)

final_file = open('per_country_common_probes.json', 'w')
final_file.write(dumps(final_dict))
final_file.close()