from ripe.atlas.cousteau import Ping, AtlasSource, AtlasCreateRequest
from datetime import datetime
from tldextract import extract

ATLAS_API_KEY = "f00d3214-a18e-4f6d-8188-104dd1192b36"

# File containing all the subdomains
f = open('./subdomains.txt', 'r')

# Populate the target list
lines = f.readlines()
targets = list()
for target in lines:
    targets.append(target)

# String to store the request Ids
req_ids = []

blocked_list = ['absa', 'standardbank', 'supersport']
_tags = {'include': ['system-ipv4-works']}
probe = AtlasSource(type='probes', value='22778', requested=1, tags=_tags)

# Prepend the earlier IDs
req_ids = []
temp_f = open('./ping_requests_ids', 'r')
line = temp_f.readline()
if line:
    req_ids = [int(v) for v in list(line[1:-1].split(','))]
else:
    req_ids = []
temp_f.close()


oldlen = 0
while targets and len(targets) != 0 and oldlen != len(targets):
    oldlen = len(targets)
    for _domain in targets:
        print(_domain)
        if extract(_domain).domain not in blocked_list:
            msm = Ping(af=4, target=_domain, description='New Ping to ' + _domain)
            atlas_request = AtlasCreateRequest(
                start_time=datetime.utcnow(),
                key=ATLAS_API_KEY,
                is_oneoff=True,
                measurements=[msm],
                sources=[probe],
            )
            (is_success, response) = atlas_request.create()
            if is_success:
                print(response['measurements'])
                req_ids += response['measurements']
                targets.remove(_domain)
            else:
                print(str(response))

# File to store the request_ids
of = open('./ping_requests_ids', 'w')
# Write the request Ids
of.write(str(req_ids))
of.close()

oof = open('./remaining_subdomains.txt', 'w')
oof.write('\n'.join(targets))
oof.close()

f.close()
