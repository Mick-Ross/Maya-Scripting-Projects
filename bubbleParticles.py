import maya.cmds as cmd
import math
# sources:
    # Referenced paper:
# https://www.glassner.com/wp-content/uploads/2014/04/CG-CGA-PDF-00-11-Soap-Bubbles-2-Nov00.pdf
    # Boolean modifiers for Constructive Solid Geometry (CSG)
# https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2020/ENU/Maya-Modeling/files/GUID-9467513F-47C3-4C73-8251-6FF8C0DE4982-htm.html


### HELPER METHODS ###

# must sort rA, rB, rD in descending order! 
def getRadGhost(bigRad, smallRad) {
    return (bigRad*smallRad)/(bigRad - smallRad)
}

def getDistBubCenters(bigRad, smallRad) {
    return sqrt(bigRad*bigRad + smallRad*smallRad - bigRad*smallRad)
}

def getDistBigToGhost(bigRad, ghostRad) {
    return sqrt(bigRad*bigRad + ghostRad*ghostRad + bigRad*ghostRad)
}

### MAIN ###

# TODO: implement Maya UI support to accept 3 radii
# hard code in radii values

radA = 3.2
radB = 2.1
radD = 0.3

## May want to clean up this redundant code
# find bubble C, modifies A and B
distAB = getDistBubCenters(radA, radB)
radCGhost = getRadGhost(radA, radB)
distAC = getDistBigToGhost(radA, radCGhost)

# find bubble E, modifies A and D
distAD = getDistBubCenters(radA, radD)
radEGhost = getRadGhost(radA, radD)
distAE = getDistBigToGhost(radA, radEGhost)

# find bubble F, modifies B and D
distBD = getDistBubCenters(radB, radD)
radFGhost = getRadGhost(radB, radD)
distBF = getDistBigToGhost(radB, radFGhost)