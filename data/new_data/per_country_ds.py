
# coding: utf-8

# In[21]:

f_list = ['countrywise_dns.json', 'countrywise_ping.json', 'countrywise_trace.json']
import json
for f_index in f_list:
    f = open(f_index, 'r')
    data_dict = json.load(f)
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
    final_file = open('intersected_' + f_index, 'w')
    final_file.write(json.dumps(final_dict))
    final_file.close()


# In[29]:

ping_file = open('intersected_countrywise_ping.json', 'r')
dns_file = open('intersected_countrywise_dns.json', 'r')
trace_file = open('intersected_countrywise_trace.json', 'r')
ping_dict = json.load(ping_file)
dns_dict = json.load(dns_file)
trace_dict = json.load(trace_file)
final_dict = dict()
for country in ping_dict:
    if country in dns_dict and country in trace_dict:
        final_dict[country] = list(set(set(ping_dict[country]).intersection(set(dns_dict[country]))).intersection(set(trace_dict[country])))


# In[30]:
final_file = open('all_three_intersection.json', 'w')
final_file.write(json.dumps(final_dict))
final_file.close()

