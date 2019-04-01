##  Author:  Ben Tannenwald
##  Date:    April 1, 2019
##  Purpose: Class to hold functions for testing higgs reconstruction algorithms and outputting .csv file for ML training

import uproot, uproot_methods
import uproot_methods.classes.TLorentzVector as TLorentzVector
import matplotlib.pyplot as plt
import numpy as np
import itertools
import csv
import copy

#t = 0.7  # transparency of plots

class eventReconstruction:
    
    def __init__ (self, _inputFile, _isTestRun = False):
        self.inputFile = _inputFile
        self.isTestRun = _isTestRun

        # class defaults
        self.transparency = 0.5  # transparency of plots
        self.dR_cut_quarkToJet = 0.40
        self.mass_higgs = 125.0 #GeV
        self.width_higgs = 15.0 #GeV, reco width
        self.minJetPt = 20.0 #GeV
        self.maxJetAbsEta = 2.5

    ##############################################################
    ##                FUNCTIONS FOR PLOTTING                    ##
    ##############################################################

    def compareManyHistograms(self, _dict, _labels, _nPlot, _title, _xtitle, _xMin, _xMax, _nBins, _normed=False):
        #_mean_arrAll     = np.mean(_arrAll)
        #_stdev_arrAll    = np.std(_arrAll)
        #_nEntries_arrAll = len(_arrAll)
        #s1 = _xtitle + ':Entries = {0}, mean = {1:4F}, std dev = {2:4f}\n'.format(_nEntries_arrAll, _mean_arrAll, _stdev_arrAll)
        
        if len(_dict.keys()) < len(_labels):
            print ("!!! Unequal number of arrays and labels. Learn to count better.")
            return 0
    
        plt.figure(_nPlot)
        if _normed:
            plt.title(_title + ' (Normalized)')
        else:
            plt.title(_title)
        plt.xlabel(_xtitle)
        _bins = np.linspace(_xMin, _xMax, _nBins)
   
        for iLabel in _labels:
            plt.hist(_dict[iLabel], _bins, alpha=t, normed=_normed, label= iLabel+' Events')
        plt.legend(loc='upper right')
        #plt.text(.1, .1, s1)
    
        # store figure copy for later saving
        fig = plt.gcf()
    
        # draw interactively
        plt.show()
    
        # save an image files
        _scope    = _title.split(' ')[0].lower()
        _variable = _xtitle.lstrip('Jet Pair').replace(' ','').replace('[GeV]','')
        _allLabels = ''.join(_labels)
        _filename  = _scope + '_' + pairingAlgorithm + '_' + _allLabels + '_' + _variable
        if _normed:
            _filename = _filename + '_norm'
        fig.savefig( _filename+'.png' )

        return


    ##############################################################
    ##                FUNCTIONS FOR INDEXING                    ##
    ##############################################################

    def returnListOfTruthBQuarkIndicesByDaughters(self, _D1, _D2, _PID):
        _bQuarkIndices = []
    
        for iParticle in range(0, len(_D1)):
            if _PID[iParticle]==25:
                _daughter1 = _D1[iParticle]
                _daughter2 = _D2[iParticle]
                _daughter1_PID = _PID[daughter1]
                _daughter2_PID = _PID[daughter2]
                #print('Event ',iEvt,'has higgs at position',iParticle,'with daughter1 (',daughter1,
                #    ') of PID',daughter1_PID,'and daughter2 (',daughter2,') of PID',daughter2_PID)
                if abs(_daughter1_PID) == 5 and abs(_daughter2_PID)==5:
                    _bQuarkIndices.append(_daughter1)
                    _bQuarkIndices.append(_daughter2)
    
        return _bQuarkIndices


    def returnListOfTruthBQuarkIndicesByStatus(self, _status):
        _bQuarkIndices = []

        for iParticle in range(0, len(_status)):
            if _status[iParticle]==23:
                _bQuarkIndices.append(iParticle)

        return _bQuarkIndices

    def returnNumberAndListOfJetIndicesPassingCuts(self, _jetPt, _jetEta, _jetMass, _jetBTag, _cut_jetPt, _cut_jetEta, _requireTags=False, _ptOrdered=False):
        _jetIndices = []
        _nJets = 0
        _nBTags = 0

        for iJet in range(0, len(_jetPt)): 
            if _jetPt[iJet] > _cut_jetPt and abs(_jetEta[iJet]) < _cut_jetEta and _jetMass[iJet]>0: 
                # surpringly some jets (<1%) have negative mass. filter these out
                _nJets += 1
                if not _requireTags:
                    _jetIndices.append(iJet)
                
                if _jetBTag[iJet] == 1:
                    _nBTags += 1
                    if _requireTags: #and len(_jetIndices)<4:
                        if _ptOrdered:
                            _added = False
                            for index in range(0, len(_jetIndices)):
                                if _jetPt[iJet] > _jetPt[index] and _added==False:
                                    _jetIndices.insert(index, iJet)
                                    _added = True
                            
                            if _added == False:
                                _jetIndices.append(iJet)
                        else:
                            _jetIndices.append(iJet)
        
            #if len(_jetIndices)==4:
            #    break
            
        #print (_jetIndices)
        #print (_nJets, _nBTags, len(_jetIndices), [_jetPt[g] for g in _jetIndices])
    
        return _nJets, _nBTags, _jetIndices


    def getDictOfQuarksMatchedToJets(self, _quarkIndices, _jetIndices, _genPt, _genEta, _genPhi, _genMass, _jetPt, _jetEta, _jetPhi, _jetMass): 
        _matchedQuarksToJets = {}
        _dictOfJetVectors = {}
        _dictOfQuarkVectors = {}
    
        for iQuark in _quarkIndices:
            tlv_quark = TLorentzVector.PtEtaPhiMassLorentzVector( _genPt[iQuark], _genEta[iQuark], _genPhi[iQuark], _genMass[iQuark])
            if iQuark not in _dictOfQuarkVectors.keys():
                _dictOfQuarkVectors[iQuark] = tlv_quark
            
            for iJet in _jetIndices:
                tlv_jet = TLorentzVector.PtEtaPhiMassLorentzVector( _jetPt[iJet], _jetEta[iJet], _jetPhi[iJet], _jetMass[iJet])
                if iJet not in _dictOfJetVectors.keys():
                    _dictOfJetVectors[iJet] = tlv_jet
        
                # skip jets
                if tlv_quark.delta_r( tlv_jet) > dR_cut_quarkToJet:
                    continue

                if iQuark not in _matchedQuarksToJets.keys():
                    _matchedQuarksToJets.update({iQuark:[iJet]})
                else:
                    _matchedQuarksToJets[iQuark].append(iJet)

        return _matchedQuarksToJets, _dictOfJetVectors, _dictOfQuarkVectors
