from urllib.parse import urlparse
import math
from datetime import datetime, timedelta

from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    Dns,
    Http,
    Sslcert,
    AtlasSource,
    AtlasCreateRequest
)

ATLAS_API_KEY = "f00d3214-a18e-4f6d-8188-104dd1192b36"
target_list = []
ping_msm = []
traceroute_msm = []
dns_msm = []
http_msm = []
ssl_msm = []

#List of subdomains
with open('trace_domains.txt') as f:
    for line in f:
        if line not in target_list:
            target_list.append(line.strip('\n'))
#############################################################################################################
#   Measurements: HTTP 'needs to be tested'
#############################################################################################################
with open('./resources/result.txt') as f:
    for line in f:
        if line.startswith('http'):
            parsed = urlparse(line.strip('\n'))
            if parsed.scheme == 'https':
                _port = 443
            else:
                _port = 80
            _host = line.strip('\n')
            _query_string = parsed.params + parsed.query
            http_msm.append(Http(target=_host, port=_port, path= parsed.path, query_string=_query_string, description='HTTP request for' + line.strip('\n')))

#############################################################################################################
#   Measurements: ping, traceroute, DNS
#############################################################################################################
_paris_no = 4  # (?)
# for _domain in target_list:
#     ping_msm.append(Ping(af=4, target=_domain, description='Ping to ' + _domain))
#     traceroute_msm.append(Traceroute(af=4, target=_domain, description='Traceroute to ' + _domain,
#                                      paris=_paris_no, protocol="ICMP"))
#     dns_msm.append(Dns(af=4, query_class='IN',query_argument=_domain, query_type='A', description='DNS A request for' + _domain))

for _domain in target_list:
    ping_msm.append(Ping(af=4, target=_domain, description='Ping to ' + _domain))
    traceroute_msm.append(Traceroute(af=4, target=_domain, description='Traceroute to ' + _domain,
                                 paris=_paris_no, protocol="ICMP"))
    dns_msm.append(Dns(af=4, query_class='IN', query_argument=_domain, query_type='A', use_probe_resolver=True,
                       include_abuf=True, include_qbuf=True, prepend_probe_id=True, retry=5,
                       description='DNS A request for ' + _domain))
    ssl_msm.append(Sslcert(af=4, query_class='IN', target=_domain, description='SSL request to ' + _domain))



#############################################################################################################
#   Probes
#############################################################################################################
# append all ipv4 assigned/allocated prefixes from ftp://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-20150330
african_sources = []

# with open('./resources/delegated-afrinic-20150330.txt') as f:
#     for line in f:
#         if line.split('|')[2] == 'ipv4':
#             _cidr_mask = 32 - int(math.log(int(line.split('|')[4]), 2))
#             _prefix = line.split('|')[3] + '/' + str(_cidr_mask)
#             _tags = {"include": ["system-ipv4-works"]}
#             african_sources.append(AtlasSource(type="prefix", value=_prefix, requested=1, tags=_tags))

# african_cc_tlds = {'DZ': 0, 'EG': 2, 'SD': 3, 'NG': 4, 'TZ': 12, 'ZA': 76, 'GH': 3, 'SN': 4, 'CM': 4, 'ZM': 5,
#                    'ZW': 3, 'SZ': 1, 'BJ': 9, 'MA': 3}

african_cc_tlds = {'EG': 2, 'SD': 3, 'NG': 4, 'TZ': 12, 'ZA': 20, 'GH': 3, 'SN': 4, 'CM': 4, 'ZM': 5,
                   'ZW': 3, 'SZ': 1, 'BJ': 9, 'MA': 3}


_tags = {"include": ["system-ipv4-works"]}
for cc, _request in african_cc_tlds.items():
    african_sources.append(AtlasSource(type="country", value=cc, requested=_request, tags=_tags))

# country code tlds: number of probes in each country. CC - Country Code.
cc_tlds = {'CN':5,'IN':5,  'JP':3, 'AU':4, 'SE':3, 'AE':2, 'TR':2, 'BY':2, 'IT':3, 'CZ':2, 'GB':4, 'ES':3,
           'US':5, 'BR':4}

non_african_sources = []
_tags = {"include": ["system-ipv4-works"]}

for cc, _request in cc_tlds.items():
    non_african_sources.append(AtlasSource(type="country", value=cc, requested=_request, tags=_tags))

#############################################################################################################
#   Creating actual request
#############################################################################################################
# File to store the req Ids
f = open("result", "w")

# Such a shame. For now we will have to start one request at a time.
# Scan the msm lists, creating measurements all along.

# Ping MSM creation
# List to store the ping measurement results.
# ping_msm_results = []
# for msm in ping_msm:
#     atlas_request = AtlasCreateRequest(
#         start_time=datetime.utcnow(),
#         key=ATLAS_API_KEY,
#         is_oneoff=True,
#         measurements=[msm],
#         sources=african_sources + non_african_sources,
#     )
#     (is_success, response) = atlas_request.create()
#     if is_success:
#         ping_msm_results += response['measurements']
#     else:
#         print(str(response))

# # List to store the dns measurement results.
# dns_msm_results = []
# for msm in dns_msm:
#     atlas_request = AtlasCreateRequest(
#         start_time=datetime.utcnow(),
#         key=ATLAS_API_KEY,
#         is_oneoff=True,
#         measurements=[msm],
#         sources=african_sources + non_african_sources,
#     )
#     (is_success, response) = atlas_request.create()
#     if is_success:
#         dns_msm_results += response['measurements']
#     else:
#         print(str(response))

#List to store the traceroute measurement results.
traceroute_msm_results = []
for msm in traceroute_msm:
    atlas_request = AtlasCreateRequest(
        start_time=datetime.utcnow(),
        key=ATLAS_API_KEY,
        is_oneoff=True,
        measurements=[msm],
        sources=african_sources + non_african_sources,
    )
    (is_success, response) = atlas_request.create()
    if is_success:
        traceroute_msm_results += response['measurements']
    else:
        print(str(response))
#
# #List to store the ssl measurement results.
# ssl_msm_results = []
# for msm in ssl_msm:
#     atlas_request = AtlasCreateRequest(
#         start_time=datetime.utcnow(),
#         key=ATLAS_API_KEY,
#         is_oneoff=True,
#         measurements=[msm],
#         sources=african_sources + non_african_sources,
#     )
#     (is_success, response) = atlas_request.create()
#     if is_success:
#         ssl_msm_results += response['measurements']
#     else:
#         print(str(response))

final_results = {}
# final_results["ping"] = ping_msm_results
# final_results["dns"] = dns_msm_results
final_results["traceroute"] = traceroute_msm_results
# final_results["ssl"] = ssl_msm_results

f.write(str(final_results))
# Close the result file
f.close()
