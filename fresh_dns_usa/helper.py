f = open('../fresh_dns/dns_data', 'rb')
pcl = pickle.Unpickler(f)
dns_data = pcl.load()
# dns_data is dict of domain:[list]
res = dns_data['facebook'] # List of all dictionaries (subdomain:dict)

rr = res[4]['ar-ar.facebook.com.'] # dict of {ProbeId: DNS Result}

rr[15397].responses[0].abuf.answers[0].raw_data

# Result
#{'Class': 'IN',
# 'Name': 'ar-ar.facebook.com.',
# 'RDlength': 7,
# 'TTL': 3600,
# 'Target': 'star.facebook.com.',
# 'Type': 'CNAME'}#
#
#
#
