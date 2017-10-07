from ripe.atlas.cousteau import AtlasResultsRequest

# list of measurement ids
msm_list = []
with open("result", "r") as f:
    for line in f.readlines():
        line = line.strip();
        if line[0] == '[':
            line = line[1:]
        if line[-1] == ']':
            line = line[:-1]
        for msm in line.split(', '):
            msm_list.append(msm.strip())
f.close()

# File to write the result in
f = open("msm_result.txt", "w")
for msm in msm_list:
    kwargs = dict()
    kwargs["msm_id"] = msm
    is_success, results = AtlasResultsRequest(**kwargs).create()
    if is_success:
        f.write(str(results) + "\n")
    else:
        print("Error in fetching the result")
f.close()
