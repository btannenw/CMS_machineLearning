import numpy as np
import pandas as pd
import uproot as ur
import math
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

###############################
## Start of defining functions

# get indices of leading values
def leadInd(_array):
    indLead = []
    for x in _array:
        if(len(x)>1):
            indLead.append(np.where(x==max(x)))
        else:
            indLead.append(0) # add an index of zero to the array bc it'll be irrelevant later anyway
    return indLead

# get leading values of jagged array from array of leading indices
def leadVals(_array,_indexArray):
    arrLead = []
    ifCount = 0
    elseCount = 0
    i = 0
    for x in _array:
        if(len(x)>1):
            ifCount +=1
            arrLead.append(x[_indexArray[i][0]])
            i+=1
        else: 
            elseCount +=1
            arrLead.append(x)
            i+=1
    return arrLead

# make 2 dimensional array of all attributes of each event
def getData(_ptArr, _etaArr, _phiArr, _eArr, _isMuonArr):
    dataArr = []
    for pt, eta, phi, e, im in zip(_ptArr, _etaArr, _phiArr, _eArr, _isMuonArr):
        if(im.size>0): # if the isMuon value isn't null
            if isinstance(pt, np.ndarray):
                if(pt.size>0):
                    pt=pt[0]
            if isinstance(eta, np.ndarray):
                if(eta.size>0):
                    eta=eta[0]
            if isinstance(phi, np.ndarray):
                if(phi.size>0):
                    phi=phi[0]
            if isinstance(e, np.ndarray):
                if(e.size>0):
                    e=e[0]
            dataArr.append([pt, eta, phi, e])
    return dataArr

# gets data with P^2 
def getDataWithP2(_ptArr, _etaArr, _phiArr, _eArr, _isMuonArr, _pArr):
    dataArr = []
    for pt, eta, phi, e, im, p in zip(_ptArr, _etaArr, _phiArr, _eArr, _isMuonArr, _pArr):
        if(im.size>0): # if the isMuon value isn't null
            if isinstance(pt, np.ndarray):
                if(pt.size>0):
                    pt=pt[0]
            if isinstance(eta, np.ndarray):
                if(eta.size>0):
                    eta=eta[0]
            if isinstance(phi, np.ndarray):
                if(phi.size>0):
                    phi=phi[0]
            if isinstance(e, np.ndarray):
                if(e.size>0):
                    e=e[0]
            if isinstance(p, np.ndarray):
                if(p.size>0):
                    p=p[0]
                    p2 = p**2
            dataArr.append([pt, eta, phi, e, p2])
    return dataArr

# gets data with P^2 and E^2
def getDataWithP2E2(_ptArr, _etaArr, _phiArr, _eArr, _isMuonArr, _pArr):
    dataArr = []
    for pt, eta, phi, e, im, p in zip(_ptArr, _etaArr, _phiArr, _eArr, _isMuonArr, _pArr):
        if(im.size>0): # if the isMuon value isn't null
            if isinstance(pt, np.ndarray):
                if(pt.size>0):
                    pt=pt[0]
            if isinstance(eta, np.ndarray):
                if(eta.size>0):
                    eta=eta[0]
            if isinstance(phi, np.ndarray):
                if(phi.size>0):
                    phi=phi[0]
            if isinstance(e, np.ndarray):
                if(e.size>0):
                    e=e[0]
                    e2=e**2
            if isinstance(p, np.ndarray):
                if(p.size>0):
                    p=p[0]
                    p2 = p**2
            dataArr.append([pt, eta, phi, e2, p2])
    return dataArr

# gets just P^2 and E^2
def getP2E2(_eArr, _isMuonArr, _pArr):
    dataArr = []
    for e, im, p in zip(_eArr, _isMuonArr, _pArr):
        if(im.size>0): # if the isMuon value isn't null
            if isinstance(e, np.ndarray):
                if(e.size>0):
                    e=e[0]
                    e2=e**2
            if isinstance(p, np.ndarray):
                if(p.size>0):
                    p=p[0]
                    p2 = p**2
            dataArr.append([e2, p2])
    return dataArr
# gets just P^2 and -E^2
def getE2P2Dec(_eArr, _isMuonArr, _pArr):
    dataArr = []
    for e, im, p in zip(_eArr, _isMuonArr, _pArr):
        if(im.size>0): # if the isMuon value isn't null
            if isinstance(e, np.ndarray):
                if(e.size>0):
                    e=e[0]
                    e2=e**2
                    e2 = e2 - (np.floor(e2)*1.000000) # these steps are because we only care about what's after the decimal point
                    e2 *= 10
            if isinstance(p, np.ndarray):
                if(p.size>0):
                    p=p[0]
                    p2 = (p**2)
                    p2 = p2 - (np.floor(p2)*1.000000)
                    p2 *= 10
            dataArr.append([e2, p2])
    return dataArr
    
## for use with getDataWithMass
# return array of tuples of Ptx and Pty
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
 
# find pz from pt and eta
def pzPtEta(_pt, _eta):
    pz = _pt*np.sinh(_eta)
    return pz

# get array of (x, y, z) tuples from xyComps and pzArr
def ptXYZ(_ptArr, _phiArr, _etaArr): #where _xyComps is an array of (x, y) tuples
    # make array of tuples (px, py, pz)
    compArr = []
    for pt, phi, eta in zip(_ptArr, _phiArr, _etaArr):
        px = np.cos(phi)*pt
        py = np.sin(phi)*pt
        pz = pzPtEta(pt, eta)
        compArr.append((px, py, pz)) # for some reason each element of this tupe is an array of length 1
    return compArr

#  get the magnitude of a vector from its components
def vMag(_x, _y, _z):
    vm = np.sqrt((_x**2)+(_y**2)+(_z**2))
    return vm

# get momentum from array of three-tuples of components
def pVals(_xyzCompArray):
    pArr = []
    for e in _xyzCompArray:
        p = vMag(e[0], e[1], e[2]) 
        pArr.append(p)
    return pArr

# get leg of a right triangle
def findLeg(_hypotenuse, _otherLeg): # now it's the pythagorean theorem and widely applicable haha
    if(_otherLeg > _hypotenuse):
        return (-1)
    else:
        l2 = np.sqrt((_hypotenuse**2)-(_otherLeg**2))
        return l2

# find mass array from arrays of energy and momentum and also hot encoded isMuon value
def findMass(_eArr, _pArr, _isMuonArr):
    massArr = []
    for e, p, im in zip(_eArr, _pArr, _isMuonArr):
        m = (findLeg(e, p), im)
        if (np.isnan(findLeg(e,p))):
            m = (-1, im) # -1 to indicate that it's a nan value
        massArr.append(m)   # in other version, this only adds if isMuon value isn't null
                            # but in this script, that's taken care of later
    return massArr

# make 2 dimensional array of all attributes of each event
def getDataWithMass(_ptArr, _etaArr, _phiArr, _eArr, _massArr, _isMuonArr):
    dataArr = []
    for pt, eta, phi, e, m, im in zip(_ptArr, _etaArr, _phiArr, _eArr, _massArr, _isMuonArr):
        if(im.size>0): # if the isMuon value isn't null
            if isinstance(pt, np.ndarray):
                if(pt.size>0):
                    pt=pt[0]
            if isinstance(eta, np.ndarray):
                if(eta.size>0):
                    eta=eta[0]
            if isinstance(phi, np.ndarray):
                if(phi.size>0):
                    phi=phi[0]
            if isinstance(e, np.ndarray):
                if(e.size>0):
                    e=e[0]
            if isinstance(m, tuple):
                m=m[0]
            dataArr.append([pt, eta, phi, e, m])
    return dataArr


# get labels where isMuon isn't null
def getLabels(_isMuonArr):
    labelArr = []
    for im in _isMuonArr:
        if(im.size>0):
            im = im[0]
            labelArr.append(im)
    return labelArr

# output array of arrays of labels
def getLabels2D(_isMuonArr):
    labelArr = []
    for im in _isMuonArr:
        if(im.size>0):
            im = im[0]
            if(im == 1):
                labelArr.append([1, 0])
            if(im == 0):
                labelArr.append([0, 1])
    return labelArr
## End of defining functions
############################

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
leptEta = ur.open("small_v2.root")["worldTree"]["eve.lepton_eta_"]
leptPhi = ur.open("small_v2.root")["worldTree"]["eve.lepton_phi_"]
leptE = ur.open("small_v2.root")["worldTree"]["eve.lepton_e_"]
leptIM = ur.open("small_v2.root")["worldTree"]["eve.lepton_isMuon_"]
leptPt = leptPt.array() # for some reason the leadV function freaks when this is done in one line
leptEta = leptEta.array()
leptPhi = leptPhi.array()
leptE = leptE.array()
leptIM = leptIM.array()


# get indices of leading values
leadIs = leadInd(leptPt)
len(leadIs)


# get array of leading values
leadPt = leadVals(leptPt, leadIs)
leadEta = leadVals(leptEta, leadIs)
leadPhi = leadVals(leptPhi, leadIs)
leadE = leadVals(leptE, leadIs)
leadIM = leadVals(leptIM, leadIs)

## Start of finding momentum 


# get array of types of ptx and pty
xyComps = []
xyComps = ptXY(leadPt, leadPhi)


# create array of three-tuples of (x,y,z)
xyzPComps = []
xyzPComps = ptXYZ(leadPt, leadPhi, leadEta)



leadP = []
leadP = pVals(xyzPComps)

## End of finding momentum 

leadM = []
leadM = findMass(leadE, leadP, leadIM)

## End of data pruning
######################

##########################################
## Data without for import in other files



# final export statements
dataNoMass = getData(leadPt, leadEta, leadPhi, leadE, leadIM)
dataWithP2 = getDataWithP2(leadPt, leadEta, leadPhi, leadE, leadIM, leadP)
dataWithP2E2 = getDataWithP2E2(leadPt, leadEta, leadPhi, leadE, leadIM, leadP)
dataWithMass = getDataWithMass(leadPt, leadEta, leadPhi, leadE, leadM, leadIM)
p2E2 = getP2E2(leadE, leadIM, leadP)
e2P2Dec = getE2P2Dec(leadE, leadIM, leadP)
labels = getLabels(leadIM)
labels2D = getLabels2D(leadIM)

## End of getting data for import in other files
################################################

