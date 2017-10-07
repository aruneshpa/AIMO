# Python script to collect the data from the request Ids.
# Author- Arunesh Pandey
#
# The final data structure for Ping, DNS, TraceRoute-
# {
#     domain1:
#     {
#         subdomain1: {
#             probe_id1: {
#
#             },
#             probe_id2: {
#
#             }
#         },
#         subdomain2: {
#
#         }
#     },
#     domain2: {
#
#     }
# }
#
import json
import urllib.request as req
from ripe.atlas.cousteau import Measurement, Probe
from ripe.atlas.sagan import PingResult, DnsResult, TracerouteResult
import tldextract as tld
import pickle   # To dump the whole obj in file


FILE_NAME = "./final_request_ids"
probe_country_dict = dict()

# Main function
if __name__ == "__main__":

    # Write the results to respective files
    # ping_file = open("./data/ping_data", "wb")
    dns_file = open("./data/dns_data_newest", "wb")
    # trace_file = open("./data/trace_data", "wb")

    # Pickle object
    # ping_pickler = pickle.Pickler(ping_file, -1)
    dns_pickler = pickle.Pickler(dns_file, -1)
    # trace_pickler = pickle.Pickler(trace_file, -1)

    # Read the lines and create a separate list per type
    f = open(FILE_NAME, "r")
    lines = f.readlines()
    print(lines)
    ping_ids = lines[0].strip().split()
    dns_ids = lines[1].strip().split()
    trace_ids = lines[2].strip().split()
    req_ids = ping_ids + dns_ids + trace_ids

    final_trace_dict = dict()    # Final Trace Route dict
    final_ping_dict = dict()    # Final Ping dict
    final_dns_dict = dict()     # Final DNS dict

    for req_id in req_ids:
        try:
            m = Measurement(id=req_id)
            subdomain_name = m.meta_data['target']
            # Make sure this is the correct req_id- random checks
            if m.description.startswith("Ping to"):
                print("Ping- " + str(req_id))
                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())

                # Create the per Probe Object
                probe_dict = dict()

                # Create the local per subdomain dict
                subdomain_dict = dict()
                i = 1
                for df in data_frame:
                    # Fill the Country vs Probe Dictionary
                    probe_id = df["prb_id"]
                    try:
                        p = Probe(id=probe_id)
                        probe_country_dict[probe_id] = p.country_code
                    except Exception as e:
                        print("Exception at Probe ID- " + str(probe_id))

                    probe_dict[probe_id] = PingResult(df)
                    print("Iteration Num- " + str(i))
                    i += 1
                subdomain_dict[subdomain_name] = probe_dict

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                if domain_name not in final_ping_dict:
                    final_ping_dict[domain_name] = []
                final_ping_dict[domain_name].append(subdomain_dict)
            elif m.description.startswith('DNS A request for '):
                print("DNS- " + str(req_id))
                if not subdomain_name or subdomain_name == '':
                    subdomain_name = m.meta_data['query_argument']
                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())

                # Create the per Probe Object
                probe_dict = dict()

                # Create the local per subdomain dict
                subdomain_dict = {}
                # Tester
                i = 1
                for df in data_frame:
                    # Fill the Country vs Probe Dictionary
                    probe_id = df["prb_id"]
                    try:
                        p = Probe(id=probe_id)
                        probe_country_dict[probe_id] = p.country_code
                    except Exception as e:
                        print("Exception at Probe ID- " + str(probe_id))

                    probe_dict[probe_id] = DnsResult(df)
                    print("Iteration Num- " + str(i))
                    i += 1
                subdomain_dict[subdomain_name] = probe_dict

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                if domain_name not in final_dns_dict:
                    final_dns_dict[domain_name] = []
                final_dns_dict[domain_name].append(subdomain_dict)
            elif m.description.startswith('Traceroute to '):
                print("Traceroute- " + str(req_id))

                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())
                # Create the per Probe Object
                probe_dict = dict()

                # Create the local per subdomain dict
                i = 1
                subdomain_dict = dict()
                for df in data_frame:
                    # Fill the Country vs Probe Dictionary
                    probe_id = df["prb_id"]
                    try:
                        p = Probe(id=probe_id)
                        probe_country_dict[probe_id] = p.country_code

                    except Exception as e:
                        print("Exception at Probe ID- " + str(probe_id))
                    probe_dict[probe_id] = TracerouteResult(df)
                    print("Iteration Num- " + str(i))
                    i += 1
                subdomain_dict[subdomain_name] = probe_dict
                print(subdomain_name)

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                if domain_name not in final_trace_dict:
                    final_trace_dict[domain_name] = []
                final_trace_dict[domain_name].append(subdomain_dict)
        except Exception as e:
            print("Exception at -" + str(req_id))

    # Dump the data to the files
    # ping_pickler.dump(final_ping_dict)
    dns_pickler.dump(final_dns_dict)
    # trace_pickler.dump(final_trace_dict)

    # File to save the probe country code
    probe_file = open("./data/probe_country_code.json", "w")
    probe_file.write(json.dumps(probe_country_dict))
    probe_file.close()

    # Close the files
    # ping_file.close()
    dns_file.close()
    # trace_file.close()
