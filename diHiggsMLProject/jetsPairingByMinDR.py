import uproot
import uproot_methods.classes.TLorentzVector as TLorentzVector
import matplotlib.pyplot as plt
import numpy as np

t = 0.7  # transparency of plots

#jet_ppTo4b_0PU = uproot.open('ppTo4b_QCD_14TeV_delphes_events.root')['Delphes']['Jet']
jet_ppToHHto4b_0PU = uproot.open('ppToHHto4b_14TeV_delphes_events.root')['Delphes']['Jet']

# ---------------------------------------------------------------------------------------------------------------------

def calc_dR(eta1, eta2, phi1, phi2):
    return ((eta1 - eta2) ** 2 + (phi1 - phi2) ** 2) ** (1 / 2)

def findMin(list):
    '''return '''
    if len(list) == 0:
        return []
    min_num = float('inf')
    i = -1
    j = -1
    for element in list:
        if element[0] < min_num:
            min_num = element[0]
            i = element[1]
            j = element[2]
    return [i, j]


def create_dR_lists(eta_event, phi_event):
    ''' returns list of dR values for all combinations of eta and phi'''
    dR_list = []
    for i in range(len(eta_event) - 1):
        for j in range(i + 1, len(eta_event)):
            dR = calc_dR(eta_event[i], eta_event[j], phi_event[i], phi_event[j])
            dR_list.append([dR, i, j])
    return dR_list


def min_dR_pairs(jet_eta, jet_phi):
    '''given a set of jet eta values and jet phi values,
    returns a list of list of jet pairs in each event based on smallest dR'''
    all_pairs = []
    for i in range(len(jet_eta)):
        dR_list = create_dR_lists(jet_eta[i], jet_phi[i])
        first_pair = findMin(dR_list)
        # remove all pair combos that are already in the first pair found
        dR_list = [i for i in dR_list if i[1] not in first_pair and i[2] not in first_pair]
        second_pair = findMin(dR_list)
        all_pairs.append([first_pair, second_pair])

    return all_pairs


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
    plt.text(400, 40, s1)
    plt.show()

# ---------------------------------------------------------------------------------------------------------------------



# choose events that have at least 4 jets and b tagged
mass_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.Mass']).tolist()
pt_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.PT']).tolist()
eta_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.Eta']).tolist()
phi_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.Phi']).tolist()
btag_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.BTag']).tolist()
id_events = uproot.tree.TBranchMethods.array(jet_ppToHHto4b_0PU['Jet.fUniqueID']).tolist()

good_events_indexes = []

for i in range(len(mass_events)):
    if len(mass_events[i]) == 4:
        tag1 = btag_events[i][0]
        tag2 = btag_events[i][1]
        tag3 = btag_events[i][2]
        tag4 = btag_events[i][3]
        if tag1 == 1 and tag2 == 1 and tag3 == 1 and tag4 == 1 :
            good_events_indexes.append(i)

good_events_mass = []
good_events_pt = []
good_events_eta = []
good_events_phi = []

for event_num in good_events_indexes:
    good_events_mass.append(mass_events[event_num])
    good_events_pt.append(pt_events[event_num])
    good_events_eta.append(eta_events[event_num])
    good_events_phi.append(phi_events[event_num])


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

dihiggs_mass = []
for event in range(jets1.shape[0]):
    mHH = (jets1[event] + jets2[event] + jets3[event] + jets4[event]).mass
    dihiggs_mass.append(mHH)


pairs = min_dR_pairs(good_events_eta, good_events_phi)


all_jets = [jets1, jets2, jets3, jets4]
all_jets = np.array(all_jets)

paired_higgs_mass = []
for i in range(len(pairs)):
    pair1 = pairs[i][0]
    pair2 = pairs[i][1]
    mH1 = (all_jets[pair1[0]][i] + all_jets[pair1[1]][i]).mass
    mH2 = (all_jets[pair2[0]][i] + all_jets[pair2[1]][i]).mass
    paired_higgs_mass.append(mH1)
    paired_higgs_mass.append(mH2)

paired_higgs_mass = np.array(paired_higgs_mass)
dihiggs_mass = np.array(dihiggs_mass)


#plot_histos(dihiggs_mass, 1, "Mass of 2 Higgs with 4 B jets", "Higgs Mass (GeV)", 0, 1000, 100)
plot_histos(paired_higgs_mass, 1, "Mass of 1 Higgs with paired B Jets based on min dR", "Higgs Mass (GeV)", 0, 1000, 100)



