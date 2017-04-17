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
    ping_file = open("./data/ping_data", "wb")
    dns_file = open("./data/dns_data", "wb")
    trace_file = open("./data/trace_data", "wb")

    # Pickle object
    ping_pickler = pickle.Pickler(ping_file, -1)
    dns_pickler = pickle.Pickler(dns_file, -1)
    trace_pickler = pickle.Pickler(trace_file, -1)

    # Read the lines and create a separate list per type
    f = open(FILE_NAME, "r")
    lines = f.readlines()
    ping_ids = lines[0]
    dns_ids = lines[1]
    trace_ids = lines[2]

    final_trace_dict = dict()    # Final Trace Route dict
    final_ping_dict = dict()    # Final Ping dict
    final_dns_dict = dict()     # Final DNS dict

    for req_id in ping_ids.strip().split():
        try:
            m = Measurement(id=req_id)
            subdomain_name = m.meta_data['target']
            # Make sure this is the correct req_id- random checks
            if m.description.startswith("Ping to"):
                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())

                # Create the per Probe Object
                probe_dict = dict()

                # Create the local per subdomain dict
                subdomain_dict = dict()
                for df in data_frame:
                    # Fill the Country vs Probe Dictionary
                    probe_id = df["prb_id"]
                    try:
                        p = Probe(id=probe_id)
                        probe_country_dict[probe_id] = p.country_code
                    except Exception as e:
                        print("Exception at Probe ID- " + str(probe_id))

                    probe_dict[probe_id] = PingResult(df)
                subdomain_dict[subdomain_name] = probe_dict

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                final_ping_dict[domain_name] = subdomain_dict
            elif m.description.startswith("DNS A request for"):
                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())

                # Create the local per subdomain dict
                subdomain_dict = {}
                for df in data_frame:
                    # Create the per Probe Object
                    probe_dict = dict()

                    # Fill the Country vs Probe Dictionary
                    probe_id = df["prb_id"]
                    p = Probe(id=probe_id)
                    probe_country_dict[probe_id] = p.country_code

                    probe_dict[probe_id] = DnsResult(df)
                subdomain_dict[subdomain_name] = probe_dict

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                final_dns_dict[domain_name] = subdomain_dict
            elif m.description.startswith("Traceroute to "):
                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())

                # Create the local per subdomain dict
                subdomain_dict = {}
                for df in data_frame:
                    # Create the per Probe Object
                    probe_dict = dict()

                    # Fill the Country vs Probe Dictionary
                    probe_id = df["prb_id"]
                    p = Probe(id=probe_id)
                    probe_country_dict[probe_id] = p.country_code

                    probe_dict[probe_id] = TracerouteResult(df)
                subdomain_dict[subdomain_name] = probe_dict

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                final_trace_dict[domain_name] = subdomain_dict
        except Exception as e:
            print("Exception at -" + str(req_id))

    # Dump the data to the files
    ping_pickler.dump(final_ping_dict)
    dns_pickler.dump(final_dns_dict)
    trace_pickler.dump(final_trace_dict)

    # Close the files
    ping_file.close()
    dns_file.close()
    trace_file.close()
