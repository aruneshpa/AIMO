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
from ripe.atlas.cousteau import Measurement
from ripe.atlas.sagan import PingResult
import tldextract as tld
import pickle   # To dump the whole obj in file


FILE_NAME = "./ping_requests_ids"
probe_country_dict = dict()

# Main function
if __name__ == "__main__":

    # Read the lines and create a separate list per type
    f = open(FILE_NAME, "r")
    line = f.readline()
    req_ids = [int(v) for v in list(line[1:-1].split(','))]
    f.close()

    final_usa_ping_dict = dict()     # Final DNS dict

    for req_id in req_ids:
        try:
            m = Measurement(id=req_id)
            subdomain_name = m.target
            # Make sure this is the correct req_id- random checks
            if m.type == 'ping' and m.description.startswith('New Ping to'):
                print("Ping- " + str(req_id))
                # Get the result string in a JSON
                url = m.result_url
                url_handle = req.urlopen(url)
                data_frame = json.loads(url_handle.read().decode())

                probe_dict = dict()

                # Create the local per subdomain dict
                subdomain_dict = dict()
                # Tester
                i = 1
                for df in data_frame:
                    probe_id = df["prb_id"]
                    probe_dict[probe_id] = PingResult(df)
                    print("Iteration Num- " + str(i))
                    i += 1
                subdomain_dict[subdomain_name] = probe_dict

                # Fill up the domain-subdomain dict
                domain_name = tld.extract(subdomain_name).domain
                if domain_name not in final_usa_ping_dict:
                    final_usa_ping_dict[domain_name] = []
                    final_usa_ping_dict[domain_name].append(subdomain_dict)
        except Exception as e:
            print("Exception at -" + str(req_id))

    # Write the results to respective files
    ping_usa_file = open("./ping_usa_data", "wb")
    # Pickle object
    ping_usa_pickler = pickle.Pickler(ping_usa_file, -1)
    # Dump the data to the files
    ping_usa_pickler.dump(final_usa_ping_dict)

    # File to save the probe country code
    probe_file = open("./probe_country_code.json", "w")
    probe_file.write(json.dumps(probe_country_dict))
    probe_file.close()

    # Close the files
    ping_usa_file.close()
