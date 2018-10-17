# import stuff
import numpy as np
import pandas as pd
import uproot as ur
import math
from matplotlib import pyplot as plt


########################
## Start of data pruning

# get tree
file = ur.open("small_v2.root")
file.allkeys()

# get branch
tree = ur.open("small_v2.root")["worldTree"]
tree.allkeys()

# get branches as arrays
leptPt = ur.open("small_v2.root")["worldTree"]["eve.lepton_pt_"]
leptPt = leptPt.array() # for some reason the leadV function freaks when this is done in one line
leptEta = ur.open("small_v2.root")["worldTree"]["eve.lepton_eta_"]
leptEta = leptEta.array()
leptPhi = ur.open("small_v2.root")["worldTree"]["eve.lepton_phi_"]
leptPhi = leptPhi.array()
leptE = ur.open("small_v2.root")["worldTree"]["eve.lepton_e_"]
leptE = leptE.array()
leptIM = ur.open("small_v2.root")["worldTree"]["eve.lepton_isMuon_"]
leptIM = leptIM.array()

# define function to get indices of leading values
def leadInd(_array):
    indLead = []
    for x in _array:
        if(len(x)>1):
            indLead.append(np.where(x==max(x)))
        else:
            indLead.append(0) # add an index of zero to the array bc it'll be irrelevant later anyway
    return indLead

# get indices of leading values
leadIs = leadInd(leptPt)
len(leadIs)

# defines function to get leading values of jagged array from array of leading indices
def leadVals(_array,_indexArray):
    arrLead = []
    ifCount = 0
    elseCount = 0
    i = 0
    for x in _array:
        if(len(x)>1):
            ifCount +=1
            arrLead.append(x[_indexArray[i]])
            i+=1
        else: 
            elseCount +=1
            arrLead.append(x)
            i+=1
    print("if, else, sum: ", ifCount, ", ",elseCount, ", ", ifCount+elseCount)
    return arrLead

# get array of leading values
leadPt = leadVals(leptPt, leadIs)
leadEta = leadVals(leptEta, leadIs)
leadPhi = leadVals(leptPhi, leadIs)
leadE = leadVals(leptE, leadIs)
leadIM = leadVals(leptIM, leadIs)
print("Number of values in each of Pt: ", len(leadPt), ", Eta: ", len(leadEta), ", Phi: ", len(leadPhi), ", E: ", len(leadE), "Lead IM: ", len(leadIM))

## End of data pruning
######################

############################
## Start of finding momentum 

# defines function to return array of tuples of Ptx and Pty
def ptXY(_ptArr, _phiArr):
    compArr = []
    i = 0
    for j in _ptArr:
        pt = j
        phi = _phiArr[i]
        ptx = np.cos(phi)*pt
        pty = np.sin(phi)*pt
        i+=1
        compArr.append((ptx,pty))
    return compArr
 
# get array of types of ptx and pty
xyComps = []
xyComps = ptXY(leadPt, leadPhi)
print("number of (x,y) tuples: ", len(xyComps))

# print (x,y)
for i in range(5):
    print(xyComps[i])

#define function to find pz from pt and eta
def pzPtEta(_pt, _eta):
    pz = _pt*np.sinh(_eta)
    return pz
#define function to get array of (x, y, z) tuples from xyComps and pzArr
def ptXYZ(_ptArr, _phiArr, _etaArr): #where _xyComps is an array of (x, y) tuples
# make array of tuples (px, py, pz)
    compArr = []
    for pt, phi, eta in zip(_ptArr, _phiArr, _etaArr):
        px = np.cos(phi)*pt
        py = np.sin(phi)*pt
        pz = pzPtEta(pt, eta)
        compArr.append((px, py, pz))
    return compArr
# create array of three-tuples of (x,y,z)
xyzPComps = []
xyzPComps = ptXYZ(leadPt, leadPhi, leadEta)

print("THE FOLLOWING IS RIGHT IF THE X AND Y VALUES MATCH THE ONES FROM ptXY!!")
# print (x,y,z)
for i in range(5):
    print(xyzPComps[i])

# define function to get the magnitude of a vector from a three-tuple of its components
def vMag(_x, _y, _z):
    vm = np.sqrt((_x**2)+(_y**2)+(_z**2))
    return vm

print(vMag(xyzPComps[0][0],xyzPComps[0][1], xyzPComps[0][2]))

def pVals(_xyzCompArray):
    pArr = []
    for e in _xyzCompArray:
        p = vMag(e[0], e[1], e[2])
        pArr.append(p)
    return pArr

leadP = []
leadP = pVals(xyzPComps)

for i in range(5):
    print(leadP[i])

## End of finding momentum 
##########################

## PLOT BREAK!!!
ptArray = tree["eve.lepton_pt_"].array()
myList = []
for x in ptArray:
    for y in x:
        if y < 300:
            myList.append(y)

print(len(myList))



# plt.hist(myList, bins=100)
# plt.title("Frequency of Lepton Transverse Momentum Values")
# plt.show()

# Okay now back to business 

########################
## Start of finding mass

# m^2 = E^2 - p^2
# leadP is the array of momentum values for each collision selected by the data pruning
# leadE is the array of energy values for each collision selected by the data pruning

# function to get mass from an energy value and a momentum value

#THIS IS ALL BROKEN !! ALL OF IT !!
for i in range(5):
    print(leadE[i])

def findLeg(_hypotenuse, _otherLeg): # now it's the pythagorean theorem and widely applicable haha
    if(_otherLeg > _hypotenuse):
        return (-1)
    else:
        l2 = np.sqrt((_hypotenuse**2)-(_otherLeg**2))
        return l2

def findMass(_eArr, _pArr, _isMuonArr):
    massArr = []
    for e, p, im in zip(_eArr, _pArr, _isMuonArr):
        m = (findLeg(e, p), im)
        if (np.isnan(findLeg(e,p))):
            m = (-1, im) # -1 to indicate that it's a nan value
        massArr.append(m)
    return massArr

def containsNAN(_list):
    for i in _list:
        if(not all(i)==True):
            return True
    return False



leadM = []
leadM = findMass(leadE, leadP, leadIM)

for i in range(5):
    print(leadM[i])

print("length of leadM: ", len(leadM))
print("leadM contains nan: ", containsNAN(leadM))

plotMass = []
numValues = 500
for i in range(numValues):
    if(leadM[i][0]>0):
        plotMass.append(leadM[i][0])
    # else:
    #     plotMass.append(0)

def isMuon(_mass):
    if(_mass > .1):
        return 1
    elif(_mass > -1):
        return 0
    else:
        return -1

# amount of electrons vs muons
eAnna = [] # electrons as determined by anna
mAnna = [] # muons as determined by anna
for i in leadM:
    if(isMuon(i[0])==1):
        mAnna.append(i)
    elif(isMuon(i[0])==0):
        eAnna.append(i)

eSmallCount = 0 # number of electrons as determined by small_v2
mSmallCount = 0 # number of muons as determined by small_v2
for i in leadIM:
    if(i==1):
        mSmallCount = mSmallCount + 1
    elif(i==0):
        eSmallCount = eSmallCount + 1

def nanMassLept(_massArr):
    nanLepts = []
    for m in _massArr:
        if(m == (-1, 0)):
            nanLepts.append(0) # the null is an electron
        elif(m == (-1, 1)):
            nanLepts.append(1) # the null is a muon
    return nanLepts

nanLepts = []
nanLepts = nanMassLept(leadM)

nanMuonsCount = sum(nanLepts)
nanElectronsCount = len(nanLepts)-sum(nanLepts)

print("AS IDENTIFIED BY ANNA: Number of muons-", len(mAnna), ". Number of electrons-", len(eAnna))
print("AS IDENTIFIED BY small_v2: Number of muons-", mSmallCount, ". Number of electrons-", eSmallCount)
print("AS IDENTIFIED BY small_v2: Number of nan muons-", nanMuonsCount, ". Number of nan electrons-", nanElectronsCount )
print("total leptons, nan or otherwise (from small_v2):", nanMuonsCount + nanElectronsCount + mSmallCount + eSmallCount)
print("NAN MUONS !!!!!!: ", nanMuonsCount)



# for i in leadM:
#     if(isMuon(i)==1):
#         plotMass.append(i)

print("number of values in plotmass:", len(plotMass))

print("number of real mass values in first", numValues, "values:", len(plotMass))

plt.hist(plotMass, bins=10)
plt.title("Frequency of Lepton Mass Values for 342 real values in first 500 values")
plt.show()


## End of finding mass
######################

