import maya.cmds as cmd
import math
from operator import add, sub
# sources:
    # Referenced paper:
# https://www.glassner.com/wp-content/uploads/2014/04/CG-CGA-PDF-00-11-Soap-Bubbles-2-Nov00.pdf
    # Boolean modifiers for Constructive Solid Geometry (CSG)
# https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2020/ENU/Maya-Modeling/files/GUID-9467513F-47C3-4C73-8251-6FF8C0DE4982-htm.html
# can redesign code around numpy arrays, may be cleaner?

### HELPER METHODS ###

# must sort rA, rB, rD in descending order! 
def getRadGhost(bigRad, smallRad):
    return (bigRad*smallRad)/(bigRad - smallRad)


def getDistBubCenters(bigRad, smallRad):
    return math.sqrt(bigRad*bigRad + smallRad*smallRad - bigRad*smallRad)

def getDistBigToGhost(bigRad, ghostRad):
    return math.sqrt(bigRad*bigRad + ghostRad*ghostRad + bigRad*ghostRad)
    
def normalize(lst):
    norm = math.sqrt(sum(i*i for i in lst))
    return list(map(lambda x: float(x)/norm, lst))

### MAIN ###

## TODO: implement Maya UI support to accept 3 radii
## hard code in radii values

## A, B, D real bubbles |||| C, E, F ghost bubbles
radA = 3.2
radB = 2.1
radD = 1.4

### May want to clean up this redundant code
## find bubble C, modifies A and B
distAB = getDistBubCenters(radA, radB)
radCGhost = getRadGhost(radA, radB)
distAC = getDistBigToGhost(radA, radCGhost)

## find bubble E, modifies A and D
distAD = getDistBubCenters(radA, radD)
radEGhost = getRadGhost(radA, radD)
distAE = getDistBigToGhost(radA, radEGhost)

## find bubble F, modifies B and D
distBD = getDistBubCenters(radB, radD)
radFGhost = getRadGhost(radB, radD)
distBF = getDistBigToGhost(radB, radFGhost)

## determine position of D
thetaA = math.acos(((distBD*distBD)-(distAB*distAB)-(distAD*distAD))/(-2*distAB*distAD))
# print(thetaA)

# we will want vec3s to define position of sphere
# bubbles defined in XY plane, A at origin
dCenter = [distAD*math.cos(thetaA), -distAD*math.sin(thetaA), 0.0]

# find position of E
dirAtoD = normalize(dCenter)
eCenter = [distAE*x for x in dirAtoD] # scalar mult

# find position of F
dirBtoD = normalize(list(map(sub, dCenter, [distAB, 0.0, 0.0])))
fCenter = list(map(add, [distAB, 0.0, 0.0], [distBF*x for x in dirBtoD]))

### FINALLY MAKE THE SPHERES
# NURBS surfaces for accuracy
bA = cmd.sphere(pivot = [0, 0, 0], axis = [0, 1, 0], radius = radA, name = "bubbleA")
bB = cmd.sphere(pivot = [distAB, 0, 0], axis = [0, 1, 0], radius = radB, name = "bubbleB")
bC = cmd.sphere(pivot = [distAC, 0, 0], axis = [0, 1, 0], radius = radCGhost, name = "bubbleCGhost")
bD = cmd.sphere(pivot = dCenter, axis = [0, 1, 0], radius = radD, name = "bubbleD")
bE = cmd.sphere(pivot = eCenter, axis = [0, 1, 0], radius = radEGhost, name = "bubbleEGhost")
bF = cmd.sphere(pivot = fCenter, axis = [0, 1, 0], radius = radFGhost, name = "bubbleFGhost")

#print(eCenter)
#print(distAE)
#print(dCenter)
#print(dirAtoD)

# CSG time
