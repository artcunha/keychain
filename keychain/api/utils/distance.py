import maya.cmds as cmds

def get_average_center(nodes):
    count = len(nodes)
    sums = [0, 0, 0]
    for node in nodes:
        pos = cmds.xform(node, q=True, ws=True, rp=True)
        sums[0] += pos[0]
        sums[1] += pos[1]
        sums[2] += pos[2]
    center = [(sums[0] / count), (sums[1] / count), (sums[2] / count)]
    return center