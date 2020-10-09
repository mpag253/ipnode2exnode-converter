import json
import sys

filename = sys.argv[1]

with open(filename, 'r') as file:
    data = json.load(file)



fields = " #Fields=1\n"

def make2char(num):
    num = int(num)
    if num >= 10:
        return str(num)
    return " " + str(num)
def sci(num): 
    if num < 0:
        return "{:.16e}".format(num).upper()
    else:
        return " {:.16e}".format(num).upper()

def isIndex(index, i):
    current = i + 1
    return current in index

def genTopNode(num):
    return " Node:           {0}\n".format(make2char(num))

def genNodes(node):
    versions = node.get('versions', -1)
    if versions == -1:
        raise Exception('no versions')
    size = len(node['all'])
    outstr = ""
    nums = node['all']
    for i in range(size):
        num = nums[i]
        if isIndex(node.get('index'), i):
            if i == 0:
                outstr += "    "
            else:
                outstr += "\n    "
            outstr += sci(num)
        else:
            if i % 5 == 0:
                outstr += "\n  "
            else:
                outstr += "  "
            outstr += sci(num)
    return outstr + "\n"
            
        
def genCoords(versions, index):
    topline = " 1) coordinates, coordinate, rectangular cartesian, #Components=3\n"
    x = "   x.  Value index={0}, #Derivatives= 3 (d/ds1,d/ds2,d2/ds1ds2)".format(make2char(index[0]))
    y = "   y.  Value index={0}, #Derivatives= 3 (d/ds1,d/ds2,d2/ds1ds2)".format(make2char(index[1]))
    z = "   z.  Value index={0}, #Derivatives= 3 (d/ds1,d/ds2,d2/ds1ds2)".format(make2char(index[2]))
    if versions > 1:
        ver = ", #Versions={0}".format(make2char(versions))
        x += ver
        y += ver
        z += ver
    x += "\n"
    y += "\n"
    z += "\n"
    return [topline,x,y,z]
    
def main(data, outfilename):

    output = [" Group name: fitted\n"]
    
    keys = data.keys()
    for key in keys:
        output.append(fields)
        node = data[key]
        
        output += genCoords(node.get('versions'), node.get('index'))
        output.append(genTopNode(key))
        output.append(genNodes(node))
    
    outstr = "".join(output)
    with open(outfilename, 'w') as file:
        file.write(outstr)

outfile = sys.argv[2]

main(data, outfile)
print("done")
