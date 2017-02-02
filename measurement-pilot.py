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

# List of subdomains
with open('./resources/domains.txt') as f:
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
            http_msm.append(Http(target=_host, port=_port, path=parsed.path, query_string=_query_string,
                                 description='HTTP request for' + line.strip('\n')))

#############################################################################################################
#   Measurements: ping, traceroute, DNS
#############################################################################################################
_paris_no = 4  # (?)
_interval = 1800
_interval = 43000

for _domain in target_list:
    # ping_msm.append(Ping(af=4, interval=_interval, target=_domain, description='Ping to ' + _domain))
    ping_msm.append(Ping(af=4, target=_domain, description='Ping to ' + _domain))
    # traceroute_msm.append(Traceroute(af=4, interval=_interval, target=_domain, description='Traceroute to ' + _domain,
    #                                  paris=_paris_no, protocol="ICMP"))
    traceroute_msm.append(Traceroute(af=4, target=_domain, description='Traceroute to ' + _domain,
                                 paris=_paris_no, protocol="ICMP"))
    # dns_msm.append(Dns(af=4, interval=_interval, query_class='IN', query_argument=_domain, query_type='A',
    #                    description='DNS A request for' + _domain))
    dns_msm.append(Dns(af=4, query_class='IN', query_argument=_domain, query_type='A',
                       description='DNS A request for' + _domain))
    ssl_msm.append(
        Sslcert(af=4, interval=_interval, query_class='IN', target=_domain, description='SSL request to ' + _domain))


#############################################################################################################
#   Probes
#############################################################################################################
# append all ipv4 assigned/allocated prefixes from ftp://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-20150330
african_sources = []

with open('./resources/delegated-afrinic-20150330.txt') as f:
    for line in f:
        if line.split('|')[2] == 'ipv4':
            _cidr_mask = 32 - int(math.log(int(line.split('|')[4]), 2))
            _prefix = line.split('|')[3] + '/' + str(_cidr_mask)
            _tags = {"include": ["system-ipv4-works"]}
            african_sources.append(AtlasSource(type="prefix", value=_prefix, requested=1, tags=_tags))
# country code tlds: number of probes in each country
african_cc_tlds = {'DZ': 1, 'EG': 1, 'SD': 1, 'NG': 1, 'TZ': 1, 'ZA': 1, 'GH': 1, 'SN': 1, 'CM': 1, 'ZM': 1, 'ZW': 1,
                   'SZ': 1, 'BJ': 1, 'MA': 1}
african_sources_pilot = []
_tags = {"include": ["system-ipv4-works"]}
for cc, _request in african_cc_tlds.items():
    african_sources_pilot.append(AtlasSource(type="country", value=cc, requested=_request, tags=_tags))

african_sources_pilot = [african_sources_pilot[1]]
"""cc_tlds = {'CN': 5, 'IN': 5, 'JP': 3, 'AU': 4, 'SE': 3, 'AE': 2, 'TR': 2, 'BY': 2, 'IT': 3, 'CZ': 2, 'UK': 4, 'ES': 3,
           'US': 5, 'BR': 4}"""
cc_tlds = {'CN': 1, 'IN': 1, 'JP': 1, 'AU': 1, 'SE': 1, 'AE': 1, 'TR': 1, 'BY': 1, 'IT': 1, 'CZ': 1, 'ES': 1,
           'US': 1, 'BR': 1}
non_african_sources = []
_tags = {"include": ["system-ipv4-works"]}

for cc, _request in cc_tlds.items():
    non_african_sources.append(AtlasSource(type="country", value=cc, requested=_request, tags=_tags))

# african_sources_pilot = [african_sources[i] for i in range(1, len(african_sources), 500)]
# non_african_sources_pilot = [non_african_sources[i] for i in range(0, len(non_african_sources), 10)]
non_african_sources_pilot = [non_african_sources[6]]

#############################################################################################################
#   Creating actual request
#############################################################################################################
atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    # stop_time=datetime.utcnow() + timedelta(days=1),  # start and end times and interval need to be decided.
    key=ATLAS_API_KEY,
    is_oneoff=True,
    measurements=dns_msm + ping_msm + traceroute_msm,
    sources=african_sources_pilot,
)
# File to store the req Ids
f = open("result", "w")

(is_success, response) = atlas_request.create()
while is_success is not True:
    print("Requests were not successful. " + str(response))
    print("Trying again!")
    (is_success, response) = atlas_request.create()
print("Request Successful! Response - " + str(response))
f.write(str(response['measurements']) + "\n")

# Close the result file
f.close()