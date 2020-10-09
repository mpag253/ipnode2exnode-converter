import json
import sys


filename = sys.argv[1]

with open(filename, 'r') as file:
    read_data = file.read()

lines = read_data.split("\n")

def getNodeNumber(line):
    words = line.split()
    num = words[-1]
    return int(num)
    
def getNumber(line):
    words = line.split()
    num = words[-1]
    return float(num)

def getVersionNumber(line):
    words = line.split()
    dirtyNum = words[-1]
    num = dirtyNum[0:-1]
    return int(num)

dic = {}
currentNode = 51
version = 0
count = 0
for i in range(len(lines)):
    line = lines[i]
    
    if "Node number" in line:
        nodeNum = getNodeNumber(line)
        currentNode = nodeNum
        dic[nodeNum] = {'versions': 0, 'index': [], 'all': []}
        count = 0
    elif "The number of versions for" in line:
        verSize = getNodeNumber(line)
        dic[currentNode]['versions'] = verSize
        if verSize == 1:
            version = 1
            dic[currentNode][version] = []
    elif "For version number" in line:
        version = getVersionNumber(line)
        dic[currentNode][version] = []
    elif "coordinate is" in line:
        count += 1
        num = getNumber(line)
        dic[currentNode]['all'].append(num)
        dic[currentNode][version].append(num)
        if version == 1:
            dic[currentNode]['index'].append(count)
    elif "The derivative wrt direction" in line:
        count += 1
        num = getNumber(line)
        dic[currentNode]['all'].append(num)
        dic[currentNode][version].append(num)
    else:
        continue
            
outfile = sys.argv[2]

with open(outfile, 'w') as file:
    json.dump(dic, file)
    
print("done")