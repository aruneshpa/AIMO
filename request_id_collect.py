# Python file to collect the data in a specified format from the request IDs
from ripe.atlas.cousteau import Measurement
start = 8136486
end = 8136501
output_file = open("final_request_ids", "r")
lines = output_file.readlines()
ping_ids = lines[0].strip()
dns_ids = lines[1].strip()
trace_ids = lines[2].strip()
output_file.close()

for i in range(start, end):
    try:
        m = Measurement(id=i)
        if m.description.startswith('Ping to'):
            print(i)
            ping_ids += str(i) + ' '
        elif m.description.startswith('DNS A request for '):
            print(i)
            dns_ids += str(i) + ' '
        elif m.description.startswith('Traceroute to '):
            print(i)
            trace_ids += str(i) + ' '
    except Exception as e:
        print("Exception - " + str(i))
        pass

output_file = open("final_request_ids", "w")
output_file.write(ping_ids + '\n' + dns_ids + '\n' + trace_ids)
output_file.close()
print("#########################")