import uproot
import uproot_methods.classes.TLorentzVector as TLorentzVector
import matplotlib.pyplot as plt
import numpy as np

t = 0.7  # transparency of plots

jet_ppTo4b_0PU = uproot.open('ppTo4b_QCD_14TeV_delphes_events.root')['Delphes']['Jet']
jet_ppToHHto4b_0PU = uproot.open('ppToHHto4b_14TeV_delphes_events.root')['Delphes']['Jet']


# ---------------------------------------------------------------------------------------------------------------------

def plot_histos(arr, nPlot, title, xtitle, xMin, xMax, nBins):
    mean_arr = np.mean(arr)
    stdev_arr = np.std(arr)
    nEntries_arr = len(arr)

    s1 = "Higgs Mass Reconstructed from 4 b-tagged jets:\n" \
         "entries = {}, mean = {:.4F}, std dev = {:.4F}".format(nEntries_arr, mean_arr, stdev_arr)

    plt.figure(nPlot)
    plt.title(title)
    plt.xlabel(xtitle)
    bins = np.linspace(xMin, xMax, nBins)
    plt.hist(arr, bins, alpha=t, label='Higgs Mass')
    plt.legend(loc='upper right')
    plt.text(10, 10, s1)
    plt.show()

# ---------------------------------------------------------------------------------------------------------------------



# choose events that have at least 4 jets and b tagged
mass_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.Mass']).tolist()
pt_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.PT']).tolist()
eta_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.Eta']).tolist()
phi_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.Phi']).tolist()
btag_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.BTag']).tolist()

good_events_mass = []
good_events_pt = []
good_events_eta = []
good_events_phi = []

for i in range(len(mass_events)):
    if len(mass_events[i]) == 4:
        tag1 = btag_events[i][0]
        tag2 = btag_events[i][1]
        tag3 = btag_events[i][2]
        tag4 = btag_events[i][3]
        if tag1 == 1 and tag2 == 1 and tag3 == 1 and tag4 == 1 :
            good_events_mass.append(mass_events[i])
            good_events_pt.append(pt_events[i])
            good_events_eta.append(eta_events[i])
            good_events_phi.append(phi_events[i])


good_events_mass = np.array(good_events_mass)
good_events_pt = np.array(good_events_pt)
good_events_eta = np.array(good_events_eta)
good_events_phi = np.array(good_events_phi)


pt1 = good_events_pt[:,0]
eta1 = good_events_eta[:,0]
phi1 = good_events_phi[:,0]
mass1 = good_events_mass[:,0]

pt2 = good_events_pt[:,1]
eta2 = good_events_eta[:,1]
phi2 = good_events_phi[:,1]
mass2 = good_events_mass[:,1]

pt3 = good_events_pt[:,2]
eta3 = good_events_eta[:,2]
phi3 = good_events_phi[:,2]
mass3 = good_events_mass[:,2]

pt4 = good_events_pt[:,3]
eta4 = good_events_eta[:,3]
phi4 = good_events_phi[:,3]
mass4 = good_events_mass[:,3]


jets1 = TLorentzVector.TLorentzVectorArray.from_ptetaphim(pt1, eta1, phi1, mass1)
jets2 = TLorentzVector.TLorentzVectorArray.from_ptetaphim(pt2, eta2, phi2, mass2)
jets3 = TLorentzVector.TLorentzVectorArray.from_ptetaphim(pt3, eta3, phi3, mass3)
jets4 = TLorentzVector.TLorentzVectorArray.from_ptetaphim(pt4, eta4, phi4, mass4)

higgs_mass = []
for event in range(jets1.shape[0]):
    mH = (jets1[event] + jets2[event] + jets3[event] + jets4[event]).mass
    higgs_mass.append(mH)


higgs_mass = np.array(higgs_mass)


plot_histos(higgs_mass, 1, "Mass of Higgs", "Higgs Mass (GeV)", 0, 1000, 100)



