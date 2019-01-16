import uproot
import heapq
import matplotlib.pyplot as plt
import skhep.math as skm
import statistics

# electron, muon and photon mass in GeV
g_mass = 0
e_mass = 0.000510998902
m_mass = 0.105658389

def findNHigest(ptlist, n):
    '''
    returns a list of the indices of the n highest elements in the np.array ptlist
    '''

    ptlist = ptlist.tolist()
    retval = []
    vals = heapq.nlargest(n, ptlist)
    for i in range(0, n):
        index = ptlist.index(vals[i])
        retval.append(index)

    return retval


def calcRecoInfo(photon_branch, electron_branch, muon_branch):
    '''
    access pt, eta, phi values from electron, muon, photon branches to calculate invariant mass
    '''

    # create lorentz vectors
    lep1 = skm.LorentzVector()
    lep2 = skm.LorentzVector()
    gamma = skm.LorentzVector()

    g_pt = uproot.tree.TBranchMethods.array(photon_branch["Photon.PT"])
    e_pt = uproot.tree.TBranchMethods.array(electron_branch["Electron.PT"])
    m_pt = uproot.tree.TBranchMethods.array(muon_branch["Muon.PT"])

    g_eta = uproot.tree.TBranchMethods.array(photon_branch["Photon.Eta"])
    e_eta = uproot.tree.TBranchMethods.array(electron_branch["Electron.Eta"])
    m_eta = uproot.tree.TBranchMethods.array(muon_branch["Muon.Eta"])

    g_phi = uproot.tree.TBranchMethods.array(photon_branch["Photon.Phi"])
    e_phi = uproot.tree.TBranchMethods.array(electron_branch["Electron.Phi"])
    m_phi = uproot.tree.TBranchMethods.array(muon_branch["Muon.Phi"])

    mass = []
    pt = []
    for i in range(0, len(electron_branch)):

        # if there is not enough information
        # if len(e_pt[i]) < 2 and len(m_pt[i]) < 2:
        if len(g_pt[i]) < 1 or (len(e_pt[i]) < 2 and len(m_pt[i]) < 2):
            continue

        if len(e_pt[i]) >= 2:
            lep_indices = findNHigest(e_pt[i], 2)
            gam_indices = findNHigest(g_pt[i], 1)
            lep1.setptetaphim(e_pt[i][lep_indices[0]], e_eta[i][lep_indices[0]], e_phi[i][lep_indices[0]], e_mass)
            lep2.setptetaphim(e_pt[i][lep_indices[1]], e_eta[i][lep_indices[1]], e_phi[i][lep_indices[1]], e_mass)
            gamma.setptetaphim(g_pt[i][gam_indices[0]], g_eta[i][gam_indices[0]], g_phi[i][gam_indices[0]], g_mass)
            # reco_mass = (lep1 + lep2 + gamma).m
            # reco_pt = (lep1 + lep2 + gamma).pt
            reco_mass = (lep1 + lep2).m
            reco_pt = (lep1 + lep2).pt
            mass.append(reco_mass)
            pt.append(reco_pt)
            print(reco_pt, lep1.pt, lep2.pt, gamma.pt)

        elif len(m_pt[i]) >= 2:
            lep_indices = findNHigest(m_pt[i], 2)
            gam_indices = findNHigest(g_pt[i], 1)
            lep1.setptetaphim(m_pt[i][lep_indices[0]], m_eta[i][lep_indices[0]], m_phi[i][lep_indices[0]], m_mass)
            lep2.setptetaphim(m_pt[i][lep_indices[1]], m_eta[i][lep_indices[1]], m_phi[i][lep_indices[1]], m_mass)
            gamma.setptetaphim(g_pt[i][gam_indices[0]], g_eta[i][gam_indices[0]], g_phi[i][gam_indices[0]], g_mass)
            # reco_mass = (lep1 + lep2 + gamma).m
            # reco_pt = (lep1 + lep2 + gamma).pt
            reco_mass = (lep1 + lep2).m
            reco_pt = (lep1 + lep2).pt
            mass.append(reco_mass)
            pt.append(reco_pt)
            print(reco_pt, lep1.pt, lep2.pt, gamma.pt)

        print("new_event")

    return mass, pt

def createMassPlots(massArray):
    '''
    takes array of masses and create matplotlib plot
    '''

    stdev = statistics.stdev(massArray)
    mean = statistics.mean(massArray)
    entries = len(massArray)

    s1 = "$\mu = {:.4F}, \ \sigma = {:.4F}$".format(mean, stdev)
    s2 = "Entries = {}".format(entries)

    plt.hist(massArray, 100, range=[0, 250])
    plt.xlabel("Mass GeV/c^2")
    plt.title("Higgs to Z Gamma 20 Pileup")  # change title when changing input file
    plt.text(60, 60, s1)
    plt.text(60, 80, s2)
    plt.show()

def createPTPlots(PTArray):
    '''
    takes array of masses and create matplotlib plot
    '''

    stdev = statistics.stdev(PTArray)
    mean = statistics.mean(PTArray)
    entries = len(PTArray)

    s1 = "$\mu = {:.4F}, \ \sigma = {:.4F}$".format(mean, stdev)
    s2 = "Entries = {}".format(entries)

    plt.hist(PTArray, 100, range=[0, 250])
    plt.xlabel("PT GeV/c")
    plt.title("Higgs to Z Gamma 20 Pileup") # change title when changing input file
    plt.text(60, 60, s1)
    plt.text(60, 80, s2)
    plt.show()


def main():
    hza20 = "hza_20pois.root"
    hza200 = "hza_200pois.root"
    dy20 = "drellyan_20pois.root"
    dy200 = "drellyan_200pois.root"
    wb20 = "wbeft_pplla20pois.root"
    wb200 = "wbeft_pplla200pois.root"
    try:
        # accessing the TTree branches
        electron_branch = uproot.open(hza20)["Delphes"]["Electron"]
        muon_branch = uproot.open(hza20)["Delphes"]["Muon"]
        photon_branch = uproot.open(hza20)["Delphes"]["Photon"]

    except FileNotFoundError:
        print("Incorrect file name - file not found")
        exit()


    mass, pt = calcRecoInfo(photon_branch, electron_branch, muon_branch)
    createMassPlots(mass)
    createPTPlots(pt)

if __name__ == "__main__":
    main()
