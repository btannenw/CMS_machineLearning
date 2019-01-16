import uproot
import matplotlib.pyplot as plt
import numpy as np

t = 0.7  # transparency of plots

def fill_histograms(h20s, h200s, d20s, d200s, w20s, w200s,
                    h20j, h200j, d20j, d200j, w20j, w200j,
                    h20m, h200m, d20m, d200m, w20m, w200m):

    print("filling...")

    hza20scht = uproot.tree.TBranchMethods.array(h20s["ScalarHT.HT"])
    hza20jpt = uproot.tree.TBranchMethods.array(h20j["Jet.PT"])
    hza20met = uproot.tree.TBranchMethods.array(h20m["MissingET.MET"])

    hza200scht = uproot.tree.TBranchMethods.array(h200s["ScalarHT.HT"])
    hza200jpt = uproot.tree.TBranchMethods.array(h200j["Jet.PT"])
    hza200met = uproot.tree.TBranchMethods.array(h200m["MissingET.MET"])

    dy20scht = uproot.tree.TBranchMethods.array(d20s["ScalarHT.HT"])
    dy20jpt = uproot.tree.TBranchMethods.array(d20j["Jet.PT"])
    dy20met = uproot.tree.TBranchMethods.array(d20m["MissingET.MET"])

    dy200scht = uproot.tree.TBranchMethods.array(d200s["ScalarHT.HT"])
    dy200jpt = uproot.tree.TBranchMethods.array(d200j["Jet.PT"])
    dy200met = uproot.tree.TBranchMethods.array(d200m["MissingET.MET"])

    wb20scht = uproot.tree.TBranchMethods.array(w20s["ScalarHT.HT"])
    wb20jpt = uproot.tree.TBranchMethods.array(w20j["Jet.PT"])
    wb20met = uproot.tree.TBranchMethods.array(w20m["MissingET.MET"])

    wb200scht = uproot.tree.TBranchMethods.array(w200s["ScalarHT.HT"])
    wb200jpt = uproot.tree.TBranchMethods.array(w200j["Jet.PT"])
    wb200met = uproot.tree.TBranchMethods.array(w200m["MissingET.MET"])


    plot_scalarht(hza20scht, hza200scht, dy20scht, dy200scht, wb20scht, wb200scht)
    plot_jpt(hza20jpt, hza200jpt, dy20jpt, dy200jpt, wb20jpt, wb200jpt)
    plot_met(hza20met, hza200met, dy20met, dy200met, wb20met, wb200met)


def plot_scalarht(h20, h200, d20, d200, w20, w200):

    h20 = np.concatenate(h20).ravel().tolist()
    d20 = np.concatenate(d20).ravel().tolist()
    w20 = np.concatenate(w20).ravel().tolist()
    h200 = np.concatenate(h200).ravel().tolist()
    d200 = np.concatenate(d200).ravel().tolist()
    w200 = np.concatenate(w200).ravel().tolist()

    meanh20 = np.mean(h20)
    stdh20 = np.std(h20)
    enth20 = len(h20)
    meanh200 = np.mean(h200)
    stdh200 = np.std(h200)
    enth200 = len(h200)

    meand20 = np.mean(d20)
    stdd20 = np.std(d20)
    entd20 = len(d20)
    meand200 = np.mean(d200)
    stdd200 = np.std(d200)
    entd200 = len(d200)

    meanw20 = np.mean(w20)
    stdw20 = np.std(w20)
    entw20 = len(w20)
    meanw200 = np.mean(w200)
    stdw200 = np.std(w200)
    entw200 = len(w200)

    s1 = "higgs z gamma:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(enth20, meanh20, stdh20)
    s2 = "drell yan:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entd20, meand20, stdd20)
    s3 = "weak boson eft:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entw20, meanw20, stdw20)
    s20 = s1 + "\n" + s2 + "\n" + s3

    s4 = "higgs z gamma:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(enth200, meanh200, stdh200)
    s5 = "drell yan:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entd200, meand200, stdd200)
    s6 = "weak boson eft:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entw200, meanw200, stdw200)
    s200 = s4 + "\n" + s5 + "\n" + s6

    plt.figure(1)
    plt.title("Scalar HT For 20 PU")
    plt.xlabel("Scalar HT")
    bins = np.linspace(0, 1000, 100)
    plt.hist(h20, bins, alpha=t, label='higgs z gamma')
    plt.hist(d20, bins, alpha=t, label='drell yan')
    plt.hist(w20, bins, alpha=t, label='weak boson eft')
    plt.legend(loc='upper right')
    plt.text(400,700,s20)
    plt.show()

    plt.figure(2)
    plt.title("Scalar HT For 200 PU")
    plt.xlabel("Scalar HT")
    bins = np.linspace(0, 1000, 100)
    plt.hist(h200, bins, alpha=t, label='higgs z gamma')
    plt.hist(d200, bins, alpha=t, label='drell yan')
    plt.hist(w200, bins, alpha=t, label='weak boson eft')
    plt.legend(loc='upper right')
    plt.text(600, 200, s200)
    plt.show()



def plot_jpt(h20, h200, d20, d200, w20, w200):

    h20 = np.concatenate(h20).ravel().tolist()
    d20 = np.concatenate(d20).ravel().tolist()
    w20 = np.concatenate(w20).ravel().tolist()
    h200 = np.concatenate(h200).ravel().tolist()
    d200 = np.concatenate(d200).ravel().tolist()
    w200 = np.concatenate(w200).ravel().tolist()

    meanh20 = np.mean(h20)
    stdh20 = np.std(h20)
    enth20 = len(h20)
    meanh200 = np.mean(h200)
    stdh200 = np.std(h200)
    enth200 = len(h200)

    meand20 = np.mean(d20)
    stdd20 = np.std(d20)
    entd20 = len(d20)
    meand200 = np.mean(d200)
    stdd200 = np.std(d200)
    entd200 = len(d200)

    meanw20 = np.mean(w20)
    stdw20 = np.std(w20)
    entw20 = len(w20)
    meanw200 = np.mean(w200)
    stdw200 = np.std(w200)
    entw200 = len(w200)

    s1 = "higgs z gamma:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(enth20, meanh20, stdh20)
    s2 = "drell yan:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entd20, meand20, stdd20)
    s3 = "weak boson eft:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entw20, meanw20, stdw20)
    s20 = s1 + "\n" + s2 + "\n" + s3

    s4 = "higgs z gamma:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(enth200, meanh200, stdh200)
    s5 = "drell yan:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entd200, meand200, stdd200)
    s6 = "weak boson eft:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entw200, meanw200, stdw200)
    s200 = s4 + "\n" + s5 + "\n" + s6

    plt.figure(3)
    plt.title("Jet PT For 20 PU")
    plt.xlabel("Jet PT")
    bins = np.linspace(0, 250, 100)
    plt.hist(h20, bins, alpha=t, label='higgs z gamma')
    plt.hist(d20, bins, alpha=t, label='drell yan')
    plt.hist(w20, bins, alpha=t, label='weak boson eft')
    plt.legend(loc='upper right')
    plt.text(100, 6000, s20)
    plt.show()

    plt.figure(4)
    plt.title("Jet PT For 200 PU")
    plt.xlabel("Jet PT")
    bins = np.linspace(0, 250, 100)
    plt.hist(h200, bins, alpha=t, label='higgs z gamma')
    plt.hist(d200, bins, alpha=t, label='drell yan')
    plt.hist(w200, bins, alpha=t, label='weak boson eft')
    plt.legend(loc='upper right')
    plt.text(100, 20000, s200)
    plt.show()

def plot_met(h20, h200, d20, d200, w20, w200):

    h20 = np.concatenate(h20).ravel().tolist()
    d20 = np.concatenate(d20).ravel().tolist()
    w20 = np.concatenate(w20).ravel().tolist()
    h200 = np.concatenate(h200).ravel().tolist()
    d200 = np.concatenate(d200).ravel().tolist()
    w200 = np.concatenate(w200).ravel().tolist()

    meanh20 = np.mean(h20)
    stdh20 = np.std(h20)
    enth20 = len(h20)
    meanh200 = np.mean(h200)
    stdh200 = np.std(h200)
    enth200 = len(h200)

    meand20 = np.mean(d20)
    stdd20 = np.std(d20)
    entd20 = len(d20)
    meand200 = np.mean(d200)
    stdd200 = np.std(d200)
    entd200 = len(d200)

    meanw20 = np.mean(w20)
    stdw20 = np.std(w20)
    entw20 = len(w20)
    meanw200 = np.mean(w200)
    stdw200 = np.std(w200)
    entw200 = len(w200)

    s1 = "higgs z gamma:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(enth20, meanh20, stdh20)
    s2 = "drell yan:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entd20, meand20, stdd20)
    s3 = "weak boson eft:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entw20, meanw20, stdw20)
    s20 = s1 + "\n" + s2 + "\n" + s3

    s4 = "higgs z gamma:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(enth200, meanh200, stdh200)
    s5 = "drell yan:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entd200, meand200, stdd20)
    s6 = "weak boson eft:\nentries = {}, mean = {:.4F}, std dev = {:.4F}".format(entw200, meanw200, stdw200)
    s200 = s4 + "\n" + s5 + "\n" + s6

    plt.figure(5)
    plt.title("Missing ET For 20 PU")
    plt.xlabel("Missing ET")
    bins = np.linspace(0, 500, 100)
    plt.hist(h20, bins, alpha=t, label='higgs z gamma')
    plt.hist(d20, bins, alpha=t, label='drell yan')
    plt.hist(w20, bins, alpha=t, label='weak boson eft')
    plt.legend(loc='upper right')
    plt.text(100, 1000, s20)
    plt.show()

    plt.figure(6)
    plt.title("Missing ET For 200 PU")
    plt.xlabel("Missing ET")
    bins = np.linspace(0, 500, 100)
    plt.hist(h200, bins, alpha=t, label='higgs z gamma')
    plt.hist(d200, bins, alpha=t, label='drell yan')
    plt.hist(w200, bins, alpha=t, label='weak boson eft')
    plt.legend(loc='upper right')
    plt.text(200, 200, s200)
    plt.show()


def main():
    try:
        print("opening...")
        hza20scht = uproot.open("hza_20pois.root")["Delphes"]["ScalarHT"]
        hza200scht = uproot.open("hza_200pois.root")["Delphes"]["ScalarHT"]
        hza20jpt = uproot.open("hza_20pois.root")["Delphes"]["Jet"]
        hza200jpt = uproot.open("hza_200pois.root")["Delphes"]["Jet"]
        hza20met = uproot.open("hza_20pois.root")["Delphes"]["MissingET"]
        hza200met = uproot.open("hza_200pois.root")["Delphes"]["MissingET"]


        dy20scht = uproot.open("drellyan_20pois.root")["Delphes"]["ScalarHT"]
        dy200scht = uproot.open("drellyan_200pois.root")["Delphes"]["ScalarHT"]
        dy20jpt = uproot.open("drellyan_20pois.root")["Delphes"]["Jet"]
        dy200jpt = uproot.open("drellyan_200pois.root")["Delphes"]["Jet"]
        dy20met = uproot.open("drellyan_20pois.root")["Delphes"]["MissingET"]
        dy200met = uproot.open("drellyan_200pois.root")["Delphes"]["MissingET"]


        wb20scht = uproot.open("wbeft_pplla20pois.root")["Delphes"]["ScalarHT"]
        wb200scht = uproot.open("wbeft_pplla200pois.root")["Delphes"]["ScalarHT"]
        wb20jpt = uproot.open("wbeft_pplla20pois.root")["Delphes"]["Jet"]
        wb200jpt = uproot.open("wbeft_pplla200pois.root")["Delphes"]["Jet"]
        wb20met = uproot.open("wbeft_pplla20pois.root")["Delphes"]["MissingET"]
        wb200met = uproot.open("wbeft_pplla200pois.root")["Delphes"]["MissingET"]

    except FileNotFoundError:
        print("Incorrect file name - file not found")
        exit()

    fill_histograms(hza20scht, hza200scht, dy20scht, dy200scht, wb20scht, wb200scht,
                    hza20jpt, hza200jpt, dy20jpt, dy200jpt, wb20jpt, wb200jpt,
                    hza20met, hza200met, dy20met, dy200met, wb20met, wb200met)


if __name__ == "__main__":
    main()