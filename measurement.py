from urllib.parse import urlparse
import math
from datetime import datetime, timedelta

from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    Dns,
    Http,
    AtlasSource,
    AtlasCreateRequest
)

ATLAS_API_KEY = "f00d3214-a18e-4f6d-8188-104dd1192b36"
target_list = []
ping_msm = []
traceroute_msm = []
dns_msm = []
http_msm = []

#List of subdomains
with open('./resources/subdomains.txt') as f:
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
for _domain in target_list:
    ping_msm.append(Ping(af=4, interval=1800, target=_domain, description='Ping to ' + _domain))
    traceroute_msm.append(Traceroute(af=4,interval=1800,  target=_domain, description='Traceroute to ' + _domain,
                                     paris=_paris_no, protocol="ICMP"))
    dns_msm.append(Dns(af=4, interval=1800, query_class='IN',query_argument=_domain, query_type='A', description='DNS A request for' + _domain))

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

# country code tlds: number of probes in each country. CC - Country Code.
cc_tlds = {'CN':5,'IN':5,  'JP':3, 'AU':4, 'SE':3, 'AE':2, 'TR':2, 'BY':2, 'IT':3, 'CZ':2, 'UK':4, 'ES':3, 'US':5, 'BR':4}
non_african_sources = []
_tags = {"include": ["system-ipv4-works"]}

for cc, _request in cc_tlds.items():
    non_african_sources.append(AtlasSource(type="country", value=cc, requested=_request, tags=_tags))

#############################################################################################################
#   Creating actual request
#############################################################################################################
atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    stop_time=datetime.utcnow() + timedelta(days=6), # start and end times and interval need to be decided.
    key=ATLAS_API_KEY,
    measurements=ping_msm + traceroute_msm,  #HTTP measurements need special permissions
    sources=african_sources + non_african_sources,
)

(is_success, response) = atlas_request.create()
print(type(response))
if is_success:
    print(response)
else:
    print(response)
