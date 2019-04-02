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


class eventReconstruction:
    
    def __init__ (self, _inputFile, _isDihiggsMC, _isTestRun = False):
        self.inputFileName = _inputFile
        self.isTestRun     = _isTestRun
        self.isDihiggsMC   = _isDihiggsMC

        # Class Defaults
        self.transparency = 0.5  # transparency of plots
        self.dR_cut_quarkToJet = 0.40
        self.mass_higgs = 125.0 #GeV
        self.width_higgs = 15.0 #GeV, reco width
        self.minJetPt = 20.0 #GeV
        self.maxJetAbsEta = 2.5
        self.nJetsToStore = 4
        self.requireTags = True
        self.ptOrdered = True

        # Global Variables 
        self.outputDataForLearning = []
        self.outputVariableNames = self.createOutputVariableList()
        self.pairingAlgorithms = ['minHarmonicMeanDeltaR', 'closestDijetMassesToHiggs', 'equalDijetMass', 'equalDeltaR', 'dijetMasses']
        self.variableCategoryDict = {'All':[], 'Matchable':[], 'Best':[], 'Best+Matchable':[], 'Correct':[]}

        self.cutflowDict = { 'All':0, 'Matchable':0, 'Fully Matched':0, '>= 1 Pair Matched':0}
        self.jetTagCategories = ['Incl',
                                 '0jIncl', '0j0b',  
                                 '1jIncl', '1j0b', '1j1b',  
                                 '2jIncl', '2j0b', '2j1b', '2j2b', 
                                 '3jIncl', '3j0b', '3j1b', '3j2b', '3j3b', 
                                 '4jIncl', '4j0b', '4j1b', '4j2b', '4j3b', '4j4b', 
                                 '5jIncl', '5j0b', '5j1b', '5j2b', '5j3b', '5j4b', '5j5b', 
                                 '6jIncl', '6j0b', '6j1b', '6j2b', '6j3b', '6j4b', '6j5b', '6j6b',
                                 '7jIncl', '7j0b', '7j1b', '7j2b', '7j3b', '7j4b', '7j5b', '7j6b', '7j7b']

        self.plottingData = {algorithm:copy.deepcopy(self.variableCategoryDict) for algorithm in self.pairingAlgorithms}
        self.eventCounterDict = { algorithm:{category:copy.deepcopy(self.cutflowDict) for category in self.jetTagCategories} for algorithm in self.pairingAlgorithms}
        self.nBTagsPerEvent  = []
        self.nJetsPerEvent   = []

        # Per-Event Variables
        self.thisEventIsMatchable = False
        self.thisEventWasCorrectlyMatched = False
        self.nJets  = 0
        self.nBTags = 0
        self.quarkIndices  = []
        self.jetIndices    = []


        # Branch Definitions
        self.delphesFile      = uproot.rootio.TObject
        self.l_genPID         = []
        self.l_genD1          = []
        self.l_genD2          = []
        self.l_genStatus      = []
        self.l_genPt          = []      
        self.l_genEta         = []
        self.l_genPhi         = []
        self.l_genMass        = []
        self.l_jetPt          = []
        self.l_jetEta         = []
        self.l_jetPhi         = []
        self.l_jetMass        = []
        self.l_jetBTag        = []
        self.l_missingET_met  = []
        self.l_missingET_phi  = []
        self.l_scalarHT       = []


    ##############################################################
    ##                           MAIN                           ##
    ##############################################################

    def runReconstruction(self):

        self.initFileAndBranches()

        for iEvt in range(0,self.delphesFile.fEntries):
            # *** 0. Kick-out condition for testing
            if iEvt > 40 and self.isTestRun is True:
                continue
            if iEvt%2000==0:
                print("Analyzing event number",iEvt)


            # *** 1. Get truth information
            self.getTruthInformation( iEvt )

            # *** 2. Get jet reco information
            self.getRecoInformation( iEvt )
            if (self.requireTags==True and self.nBTags < 4) or (self.requireTags==False and self.nJets < 4): continue 

            # *** 3. Do some quark-to-jet truth matching
            if self.isDihiggsMC == True:
                matchedQuarksToJets, jetVectorDict, quarkVectorDict = self.truthToRecoMatching( iEvt )

            # *** 4. Evaluate all pairing algorithms
            #self.

        return
    
    ##############################################################
    ##             FUNCTIONS TO SET/GET VARIABLES               ##
    ##############################################################

    def setTransparency(self, _userTransparency):
        self.transparency = _userTransparency
    def getTransparency(self):
        print ("Transparency: ", self.transparency)
        return self.transparency

    def setNJetsToStore(self, _userNJetsToStore):
        self.nJetsToStore = _userNJetsToStore
    def getNJetsToStore(self):
        print ("N_Jets To Store: ", self.nJetsToStore)
        return self.nJetsToStore
        
    def setQuarkToJetCutDR(self, _userQuarkToJetCutDR):
        self.dR_cut_quarkToJet = _userQuarkToJetCutDR
    def getQuarkToJetCutDR(self):
        print ("DeltaR Cut Between Jet and Quark: ", self.dR_cut_quarkToJet)
        return self.dR_cut_quarkToJet

    def setHiggsMass(self, _userMassHiggs):
        self.mass_higgs = _userMassHiggs
    def getHiggsMass(self):
        print ("Higgs Mass: ", self.mass_higgs)
        return self.mass_higgs

    def setHiggsWidth(self, _userWidthHiggs):
        self.width_higgs = _userWidthHiggs
    def getHiggsWidth(self):
        print ("Higgs Width: ", self.width_higgs)
        return self.width_higgs

    def setJetPtEtaCuts(self, _userJetPtCut, _userJetEtaCut):
        self.minJetPt = _userJetPtCut #GeV
        self.maxJetAbsEta = _userJetEtaCut
    def getJetPtEtaCuts(self):
        print ("Minimum Jet pT [GeV]: ", self.minJetPt)
        print ("Maximum Jet |eta|: ", self.maxJetAbsEta)
        return self.minJetPt, self.maxJetAbsEta


    ##############################################################
    ##                FUNCTIONS FOR PLOTTING                    ##
    ##############################################################

    def compareManyHistograms(self, _pairingAlgorithm, _labels, _nPlot, _title, _xtitle, _xMin, _xMax, _nBins, _normed=False):
        #_mean_arrAll     = np.mean(_arrAll)
        #_stdev_arrAll    = np.std(_arrAll)
        #_nEntries_arrAll = len(_arrAll)
        #s1 = _xtitle + ':Entries = {0}, mean = {1:4F}, std dev = {2:4f}\n'.format(_nEntries_arrAll, _mean_arrAll, _stdev_arrAll)
        
        if len( self.plottingData[_pairingAlgorithm].keys()) < len(_labels):
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
            plt.hist(self.plottingData[_pairingAlgorithm][iLabel], _bins, alpha=self.transparency, normed=_normed, label= iLabel+' Events')
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

    def returnListOfTruthBQuarkIndicesByDaughters(self, _iEvent):
    
        for iParticle in range(0, len(_D1)):
            if self.PID[_iEvent][iParticle]==25:
                _daughter1 = self.l_genD1[_iEvent][iParticle]
                _daughter2 = self.l_genD2[_iEvent][iParticle]
                _daughter1_PID = self.l_genPID[_iEvent][daughter1]
                _daughter2_PID = self.l_genPID[_iEvent][daughter2]
                #print('Event ',iEvt,'has higgs at position',iParticle,'with daughter1 (',daughter1,
                #    ') of PID',daughter1_PID,'and daughter2 (',daughter2,') of PID',daughter2_PID)
                if abs(_daughter1_PID) == 5 and abs(_daughter2_PID)==5:
                    self.quarkIndices.append(_daughter1)
                    self.quarkIndices.append(_daughter2)
    
        return 


    def returnListOfTruthBQuarkIndicesByStatus(self, _iEvent ):

        for iParticle in range(0, len(self.l_genStatus[_iEvent]) ):
            if self.l_genStatus[_iEvent][iParticle]==23:
                self.quarkIndices.append(iParticle)

        return 

    def returnNumberAndListOfJetIndicesPassingCuts(self, _iEvent):
        self.nJets = 0
        self.nBTags = 0
        self.jetIndices = []

        for iJet in range(0, len(self.l_jetPt[_iEvent])): 
            if self.l_jetPt[_iEvent][iJet] > self.minJetPt and abs(self.l_jetEta[_iEvent][iJet]) < self.maxJetAbsEta and self.l_jetMass[_iEvent][iJet]>0: 
                # surpringly some jets (<1%) have negative mass. filter these out
                self.nJets += 1
                if not self.requireTags:
                    self.jetIndices.append(iJet)
                
                if self.l_jetBTag[_iEvent][iJet] == 1:
                    self.nBTags += 1
                    if self.requireTags: #and len(self.jetIndices)<4:
                        if self.ptOrdered:
                            _added = False
                            for index in range(0, len(self.jetIndices)):
                                if self.l_jetPt[_iEvent][iJet] > self.l_jetPt[_iEvent][index] and _added==False:
                                    self.jetIndices.insert(index, iJet)
                                    _added = True
                            
                            if _added == False:
                                self.jetIndices.append(iJet)
                        else:
                            self.jetIndices.append(iJet)
        
            #if len(_jetIndices)==4:
            #    break
            
        #print (_jetIndices)
        #print (self.nJets, self.nBTags, len(_jetIndices), [_jetPt[g] for g in _jetIndices])
    
        return 


    def getDictOfQuarksMatchedToJets(self, _iEvent ): 
        _matchedQuarksToJets = {}
        _dictOfJetVectors = {}
        _dictOfQuarkVectors = {}
    
        for iQuark in self.quarkIndices:
            tlv_quark = TLorentzVector.PtEtaPhiMassLorentzVector( self.l_genPt[_iEvent][iQuark], self.l_genEta[_iEvent][iQuark], self.l_genPhi[_iEvent][iQuark], self.l_genMass[_iEvent][iQuark])
            if iQuark not in _dictOfQuarkVectors.keys():
                _dictOfQuarkVectors[iQuark] = tlv_quark
            
            for iJet in self.jetIndices:
                tlv_jet = TLorentzVector.PtEtaPhiMassLorentzVector( self.l_jetPt[_iEvent][iJet], self.l_jetEta[_iEvent][iJet], self.l_jetPhi[_iEvent][iJet], self.l_jetMass[_iEvent][iJet])
                if iJet not in _dictOfJetVectors.keys():
                    _dictOfJetVectors[iJet] = tlv_jet
        
                # skip jets
                if tlv_quark.delta_r( tlv_jet) > self.dR_cut_quarkToJet:
                    continue

                if iQuark not in _matchedQuarksToJets.keys():
                    _matchedQuarksToJets.update({iQuark:[iJet]})
                else:
                    _matchedQuarksToJets[iQuark].append(iJet)

        return _matchedQuarksToJets, _dictOfJetVectors, _dictOfQuarkVectors


    ##############################################################
    ##                FUNCTIONS FOR MATCHING                    ##
    ##############################################################

    def getHarmonicMeanDeltaR( self, _jetPairTuple, _jetVectorDict):

        # get deltaR between each pair
        _deltaR_pair1 = _jetVectorDict[_jetPairTuple[0]].delta_r(_jetVectorDict[_jetPairTuple[1]])
        _deltaR_pair2 = _jetVectorDict[_jetPairTuple[2]].delta_r(_jetVectorDict[_jetPairTuple[3]])
        if _deltaR_pair1 == 0 or _deltaR_pair2==0:
            print('pair1',_deltaR_pair1, _jetPairTuple[0], _jetPairTuple[1], _jetVectorDict[_jetPairTuple[0]].pt, _jetVectorDict[_jetPairTuple[1]].pt)
            print('pair2',_deltaR_pair2, _jetPairTuple[2], _jetPairTuple[3], _jetVectorDict[_jetPairTuple[2]].pt, _jetVectorDict[_jetPairTuple[3]].pt)
            
        # calculate the harmonic mean
        _meanDeltaR = np.reciprocal( ( np.reciprocal(_deltaR_pair1) + np.reciprocal(_deltaR_pair2) ) / 2 )
        #print(_jetPairTuple, _meanDeltaR, _deltaR_pair1, _deltaR_pair2)

        return _meanDeltaR

    def getEqualDeltaR( self, _jetPairTuple, _jetVectorDict):

        # get deltaR between each pair
        _deltaR_pair1 = _jetVectorDict[_jetPairTuple[0]].delta_r(_jetVectorDict[_jetPairTuple[1]])
        _deltaR_pair2 = _jetVectorDict[_jetPairTuple[2]].delta_r(_jetVectorDict[_jetPairTuple[3]])
        
        # calculate the harmonic mean
        _diffDeltaR = abs( _deltaR_pair1 - _deltaR_pair2 )
        #print(_jetPairTuple, _meanDeltaR, _deltaR_pair1, _deltaR_pair2)
        
        return _diffDeltaR


    def getHiggsMassDifference( self, _jetPairTuple, _jetVectorDict):

        # get deltaR between each pair
        _mass_pair1 = ( _jetVectorDict[_jetPairTuple[0]] + _jetVectorDict[_jetPairTuple[1]] ).mass 
        _mass_pair2 = ( _jetVectorDict[_jetPairTuple[2]] + _jetVectorDict[_jetPairTuple[3]] ).mass 
        
        # calculate the quadrature sum of higgs mass diff and divide by reco higgs width
        _quadratureMassDifference = np.sqrt( ( (_mass_pair1 - mass_higgs) / width_higgs )**2 + ( (_mass_pair2 - mass_higgs) / width_higgs )**2 )
        #print(_jetPairTuple, _quadratureMassDifference, _massDiff_pair1, _massDiff_pair2)
        
        return _quadratureMassDifference


    def getDijetMassDifference( self, _jetPairTuple, _jetVectorDict):

        # get masses for each pair
        _mass_pair1 = ( _jetVectorDict[_jetPairTuple[0]] + _jetVectorDict[_jetPairTuple[1]] ).mass 
        _mass_pair2 = ( _jetVectorDict[_jetPairTuple[2]] + _jetVectorDict[_jetPairTuple[3]] ).mass 
        
        # calculate the direct difference of reco dijet masses
        _dijetMassDifference = abs(_mass_pair1 - _mass_pair2)
        #print(_jetPairTuple, _quadratureMassDifference, _massDiff_pair1, _massDiff_pair2)
        
        return _dijetMassDifference


    def getBothDijetMasses( self, _jetPairTuple, _jetVectorDict):
        
        # get masses of each pair
        _mass_pair1 = ( _jetVectorDict[_jetPairTuple[0]] + _jetVectorDict[_jetPairTuple[1]] ).mass 
        _mass_pair2 = ( _jetVectorDict[_jetPairTuple[2]] + _jetVectorDict[_jetPairTuple[3]] ).mass 
        
        # make a list of the two masses
        _bothDijetMasses = [_mass_pair1, _mass_pair2 ]
        
        return _bothDijetMasses
        
        
    def returnMetric( self, _pairingAlgorithm, _sortedTuple, _jetVectorDict):
        # calculate metric depending on chosen algorithm
        _metric = []
        
        if _pairingAlgorithm == "minHarmonicMeanDeltaR":
            _metric = getHarmonicMeanDeltaR(_sortedTuple, _jetVectorDict)
        elif _pairingAlgorithm == "closestDijetMassesToHiggs":
            _metric = getHiggsMassDifference(_sortedTuple, _jetVectorDict)
        elif _pairingAlgorithm == "equalDijetMass":
            _metric = getDijetMassDifference(_sortedTuple, _jetVectorDict)
        elif _pairingAlgorithm == "equalDeltaR":
            _metric = getEqualDeltaR(_sortedTuple, _jetVectorDict)
        elif _pairingAlgorithm == "dijetMasses":
            _metric = getBothDijetMasses(_sortedTuple, _jetVectorDict)
            
        _metric = _metric if type(_metric)==list else [_metric]
        return _metric


    def selectPairsViaMatchingAlgorithm( self, _jetVectorDict, _pairingAlgorithm):

        # make list of pairs from [n choose 2] where n is number of jets
        _jetPairs = list(itertools.combinations(_jetVectorDict.keys(),2))
        _doubleJetPairs = {}

        # loop over jet pairs
        for pair in _jetPairs:
            # make list of leftover pairs that do not contain either jet in starting pair
            _notPair = [x for x in list(_jetPairs) if pair[0] not in x and pair[1] not in x]
            for pairOption in _notPair:
                _sortedPairing = sorted([sorted(x) for x in [pair, pairOption]])
                _sortedTuple = tuple(_sortedPairing[0]+_sortedPairing[1])

                # add double pairing to dictionary if not already present. sorting removes positional ambiguity
                if _sortedTuple not in _doubleJetPairs.keys():
                    _metric = returnMetric(_pairingAlgorithm, _sortedTuple, _jetVectorDict)

                    _doubleJetPairs[_sortedTuple] = _metric
                    self.plottingData[_pairingAlgorithm]['All'].extend( _metric )
                    if thisEventIsMatchable:
                        self.plottingData[_pairingAlgorithm]['Matchable'].extend( _metric )

        # sort output dict and find minimal value
        _bestPairing = sorted(_doubleJetPairs.items(), key=lambda _pairingAndMetric: _pairingAndMetric[1][0])[0]
        self.plottingData[_pairingAlgorithm]['Best'].extend( _bestPairing[1] )   
        if thisEventIsMatchable:
            # fill algorithm-selected lists for plotting
            self.plottingData[_pairingAlgorithm]['Best+Matchable'].extend( _bestPairing[1] )


        return (_bestPairing[0][0], _bestPairing[0][1]), (_bestPairing[0][2] , _bestPairing[0][3]), _bestPairing[1][0]


    def fillVariablePlotsForCorrectPairing( self, iEvt, _matchedJetVector, _pairingAlgorithm):
        _correctTuple = (0, 1, 2, 3)
        _metric = returnMetric(_pairingAlgorithm, _correctTuple, _matchedJetVector)
        self.plottingData[_pairingAlgorithm]['Correct'].extend( _metric )
        if _metric[0]==0:
            print (iEvt)

        return

    
    ##############################################################
    ##                FUNCTIONS FOR EFFICIENCY                  ##
    ##############################################################

    def returnJetTagLabels( self ):

        # every event is inclusive
        _categoryLabels = ['Incl']    
    
        # split into tag-inclusive bins, 6j means >= 6 jets
        if self.nJets == 4:
            _categoryLabels.append('4jIncl')
        elif self.nJets == 5:
            _categoryLabels.append('5jIncl')
        elif self.nJets == 6:
            _categoryLabels.append('6jIncl')
        elif self.nJets >= 7:
            _categoryLabels.append('7jIncl')
            
        # split into tag bins, 4b means >= 4 tags
        _jetLabel = str(self.nJets) if self.nJets <= 7 else str(7)
        _tagLabel = str(self.nBTags) if self.nBTags <= 7 else str(7)
        _categoryLabels.append( _jetLabel+'j'+_tagLabel+'b' )
        
        return _categoryLabels


    def countEvents( self, _cutflowBin ):

        _categoryLabels = self.returnJetTagLabels()
        for iAlgorithm in self.eventCounterDict:
            for iLabel in _categoryLabels:
                self.eventCounterDict[iAlgorithm][iLabel][_cutflowBin] += 1
        
    
    def evaluatePairingEfficiency( self, _quarkToJetDict, _jetPair1, _jetPair2, _algorithm):
                
        # Organize quark-to-jet pairs from truth into directly comparable tuples
        _indexList = list( _quarkToJetDict.values() ) 
        _orderedIndexTuple = sorted( ( tuple(sorted( (_indexList[0][0], _indexList[1][0]) )) , tuple(sorted( (_indexList[2][0], _indexList[3][0]) )) ) )
        _indexPair1 = _orderedIndexTuple[0]
        _indexPair2 = _orderedIndexTuple[1]
        
        # Do some global counting
        _categoryLabels = self.returnJetTagLabels()
        for iLabel in _categoryLabels:
            if _jetPair1 == _indexPair1 and _jetPair2 == _indexPair2:
                self.eventCounterDict[_algorithm][iLabel]['Fully Matched'] += 1
         
            if _jetPair1 == _indexPair1 or _jetPair2 == _indexPair2:
                self.eventCounterDict[_algorithm][iLabel]['>= 1 Pair Matched'] += 1
        
        return 


        
    def printEventCounterInfo( self, _algorithm, _catTag ):
        print('====================================================')
        print("!!!! Event Counter Info For " + _algorithm + ", " + _catTag)
        print("Number of Events:", self.eventCounterDict[_algorithm][_catTag]['All'])
        print("Number of Events with 4 truth-matchable jets:", self.eventCounterDict[_algorithm][_catTag]['Matchable'])
        print("Number of Events Fully Matched:", self.eventCounterDict[_algorithm][_catTag]['Fully Matched'])
        print("Number of Events with >= 1 Pair Matched:", self.eventCounterDict[_algorithm][_catTag]['>= 1 Pair Matched'])
        if self.eventCounterDict[_algorithm][_catTag]['Matchable'] > 0:
            print('Efficiency For Fully Matched: ',round( 100*float(self.eventCounterDict[_algorithm][_catTag]['Fully Matched']/self.eventCounterDict[_algorithm][_catTag]['Matchable']) , 2),'%')
            print('Efficiency For >= 1 Pair Matched: ',round( 100*float(self.eventCounterDict[_algorithm][_catTag]['>= 1 Pair Matched']/self.eventCounterDict[_algorithm][_catTag]['Matchable']) , 2),'%')
 
        return


    def listOfEfficiencesForAlgorithm( self ):
        _fullyMatchedDict = {}
        _onePairMatchedDict = {}
    
        for _iAlgorithm in self.eventCounterDict:
            _fullyMatchedDict[_iAlgorithm] = {}
            _onePairMatchedDict[_iAlgorithm] = {}
            for _iCategory in self.eventCounterDict[_iAlgorithm]:
                if self.eventCounterDict[_iAlgorithm][_iCategory]['Matchable'] > 0:
                    _fullyMatchedEff  = round( 100*float(self.eventCounterDict[_iAlgorithm][_iCategory]['Fully Matched']/self.eventCounterDict[_iAlgorithm][_iCategory]['Matchable']), 2)
                    _onePairMatchedEff = round( 100*float(self.eventCounterDict[_iAlgorithm][_iCategory]['>= 1 Pair Matched']/self.eventCounterDict[_iAlgorithm][_iCategory]['Matchable']), 2)
                    _fullyMatchedDict[_iAlgorithm][_iCategory] = _fullyMatchedEff
                    _onePairMatchedDict[_iAlgorithm][_iCategory] = _onePairMatchedEff
                    #print(_algorithm, _iCategory)
                    #print('Efficiency For Fully Matched: ', _fullyMatchedEff,'%')
                    #print('Efficiency For >= 1 Pair Matched: ', _onePairMatchedEff,'%')
                
        return _fullyMatchedDict, _onePairMatchedDict


    ##############################################################
    ##           FUNCTIONS FOR CALCULATING BDT VARS             ##
    ##############################################################

    def createOutputVariableList( self ):
        _variableNameList = ['hh_mass', 'h1_mass', 'h2_mass', 'hh_pt', 'h1_pt', 'h2_pt', 'deltaR(h1, h2)', 'deltaR(h1 jets)', 'deltaR(h2 jets)', 'deltaPhi(h1 jets)', 'deltaPhi(h2 jets)', 'met', 'met_phi', 'scalarHT', 'nJets', 'nBTags']
        _jetVariables = ['pt', 'eta', 'phi', 'mass', 'px', 'py', 'pz', 'energy']
    
        for _variable in _jetVariables:
            _variableNameList.extend( ['jet'+str(_iJet)+'_'+str(_variable) for _iJet in range(1,self.nJetsToStore+1)])
    
        return _variableNameList


    def calculateVariablesForBDT( self, _jetPair1, _jetPair2, _jetVectorDict, _met, _met_phi, _scalarHT, _addLowLevel = False):
        _variableList = []
    
        _tlv_h1_j0 = _jetVectorDict[ _jetPair1[0] ]
        _tlv_h1_j1 = _jetVectorDict[ _jetPair1[1] ]
        _tlv_h2_j2 = _jetVectorDict[ _jetPair2[0] ]
        _tlv_h2_j3 = _jetVectorDict[ _jetPair2[1] ]
        _tlv_h1 = _tlv_h1_j0 + _tlv_h1_j1
        _tlv_h2 = _tlv_h2_j2 + _tlv_h2_j3

        """print('====================================================')
        print ("hh mass: ", (_tlv_h1 + _tlv_h2).mass)
        print ("h1 mass: ", _tlv_h1.energy, _tlv_h1.p, _tlv_h1_j0.energy, _tlv_h1_j0.p, _tlv_h1_j1.energy, _tlv_h1_j1.p)
        print ("h2 mass: ", _tlv_h2.mass)
        print ("hh pt: ", (_tlv_h1 + _tlv_h2).pt)
        print ("h1 pt: ", _tlv_h1.pt)
        print ("h2 pt: ", _tlv_h2.pt)
        print ("dR(h1, h2): ",  _tlv_h1.delta_r( _tlv_h2 ))
        print ("for h1, dR(j0, j1): ",  _tlv_h1_j0.delta_r( _tlv_h1_j1 ))
        print ("for h2, dR(j2, j3): ",  _tlv_h2_j2.delta_r( _tlv_h2_j3 ))
        print ("for h1, dPhi(j0, j1): ",  _tlv_h1_j0.delta_phi( _tlv_h1_j1 ))
        print ("for h2, dPhi(j2, j3): ",  _tlv_h2_j2.delta_phi( _tlv_h2_j3 ))
        #print ("MET, met_phi: ", _met[0], _met_phi[0])
        #print ("Scalar HT: ", _scalarHT[0])
        #print ("nJets, nBTags: ", self.nJets, self.nBTags)
        """
        _nDigits = 3
        
        _variableList = [ (_tlv_h1 + _tlv_h2).mass, _tlv_h1.mass, _tlv_h2.mass,
                          (_tlv_h1 + _tlv_h2).pt, _tlv_h1.pt, _tlv_h2.pt,
                          _tlv_h1.delta_r(_tlv_h2), 
                          _tlv_h1_j0.delta_r(_tlv_h1_j1), _tlv_h2_j2.delta_r(_tlv_h2_j3), 
                          _tlv_h1_j0.delta_phi(_tlv_h1_j1), _tlv_h2_j2.delta_phi(_tlv_h2_j3), 
                          _met[0], _met_phi[0], _scalarHT[0], 
                          self.nJets, self.nBTags,
                          _tlv_h1_j0.pt, _tlv_h1_j1.pt, _tlv_h2_j2.pt, _tlv_h2_j3.pt, 
                          _tlv_h1_j0.eta, _tlv_h1_j1.eta, _tlv_h2_j2.eta, _tlv_h2_j3.eta,
                          _tlv_h1_j0.phi, _tlv_h1_j1.phi, _tlv_h2_j2.phi, _tlv_h2_j3.phi,
                          _tlv_h1_j0.mass, _tlv_h1_j1.mass, _tlv_h2_j2.mass, _tlv_h2_j3.mass,
                          _tlv_h1_j0.x, _tlv_h1_j1.x, _tlv_h2_j2.x, _tlv_h2_j3.x, 
                          _tlv_h1_j0.y, _tlv_h1_j1.y, _tlv_h2_j2.y, _tlv_h2_j3.y, 
                          _tlv_h1_j0.z, _tlv_h1_j1.z, _tlv_h2_j2.z, _tlv_h2_j3.z, 
                          _tlv_h1_j0.energy, _tlv_h1_j1.energy, _tlv_h2_j2.energy, _tlv_h2_j3.energy
                      ]
        
        return _variableList



    ##############################################################
    ##           FUNCTIONS FOR RUNNING RECONSTRUCTION           ##
    ##############################################################


    def truthToRecoMatching( self, _iEvent, ):

        self.thisEventIsMatchable = False
        self.thisEventWasCorrectlyMatched = False
        _matchedQuarksToJets, _jetVectorDict, _quarkVectorDict = self.getDictOfQuarksMatchedToJets( _iEvent )
        # Check if a) all matches have one and only match between quark and jet, b) four jets are matched, c) 4 unique reconstructed jets are selected
        _jetIndexList = [recoIndex[0] for recoIndex in _matchedQuarksToJets.values()]
        if all(len(matchedJets) == 1 for matchedJets in _matchedQuarksToJets.values()) and len(_matchedQuarksToJets)==4  and (len(set(_jetIndexList)) == len(_jetIndexList)):     
            self.thisEventIsMatchable = True
            self.countEvents( 'Matchable' )

        return _matchedQuarksToJets, _jetVectorDict, _quarkVectorDict

    def getRecoInformation( self, _iEvent ):
        self.returnNumberAndListOfJetIndicesPassingCuts( _iEvent )
        self.nJetsPerEvent.append( self.nJets )
        self.nBTagsPerEvent.append( self.nBTags  )
        self.countEvents( 'All' )
        
        return 

    def getTruthInformation( self, _iEvent ):

        self.quarkIndices = []       
        # Return if QCD --> no truth to assign
        if self.isDihiggsMC == False:
            return

        self.returnListOfTruthBQuarkIndicesByStatus( _iEvent )   
        #self.returnListOfTruthBQuarkIndicesByDaughters( _iEvent )   

        if len( self.quarkIndices ) != 4:
            print ("!!! WARNING: Event = {0} did not find 4 truth b-quarks. Only found {1} !!!".format(iEvent, len(self.quarkIndices)))
            
        return 
    

    def initFileAndBranches( self ):

        print("Setting Delphes file; ", self.inputFileName)
        self.delphesFile= uproot.open(self.inputFileName)['Delphes']

        #b_particles = uproot.tree.TBranchMethods.array(delphes_hh['Particle'])
        self.l_genPID         = uproot.tree.TBranchMethods.array(self.delphesFile['Particle']['Particle.PID']).tolist()
        self.l_genStatus      = uproot.tree.TBranchMethods.array(self.delphesFile['Particle']['Particle.Status']).tolist()
        self.l_genPt          = uproot.tree.TBranchMethods.array(self.delphesFile['Particle']['Particle.PT']).tolist()
        self.l_genEta         = uproot.tree.TBranchMethods.array(self.delphesFile['Particle']['Particle.Eta']).tolist()
        self.l_genPhi         = uproot.tree.TBranchMethods.array(self.delphesFile['Particle']['Particle.Phi']).tolist()
        self.l_genMass        = uproot.tree.TBranchMethods.array(self.delphesFile['Particle']['Particle.Mass']).tolist()
        self.l_jetPt          = uproot.tree.TBranchMethods.array(self.delphesFile['Jet']['Jet.PT']).tolist()
        self.l_jetEta         = uproot.tree.TBranchMethods.array(self.delphesFile['Jet']['Jet.Eta']).tolist()
        self.l_jetPhi         = uproot.tree.TBranchMethods.array(self.delphesFile['Jet']['Jet.Phi']).tolist()
        self.l_jetMass        = uproot.tree.TBranchMethods.array(self.delphesFile['Jet']['Jet.Mass']).tolist()
        self.l_jetBTag        = uproot.tree.TBranchMethods.array(self.delphesFile['Jet']['Jet.BTag']).tolist()
        self.l_missingET_met  = uproot.tree.TBranchMethods.array(self.delphesFile['MissingET']['MissingET.MET']).tolist()
        self.l_missingET_phi  = uproot.tree.TBranchMethods.array(self.delphesFile['MissingET']['MissingET.Phi']).tolist()
        self.l_scalarHT       = uproot.tree.TBranchMethods.array(self.delphesFile['ScalarHT']['ScalarHT.HT']).tolist()
        print("Finished loading branches...")


"""
 # *** 4. Evaluate all pairing algorithms
    for iAlgorithm in pairingAlgorithms:
        # ** A. Fill algorithm metric for correct pairing (regardless if chosen by metric)
        if thisEventIsMatchable == True:
            fillVariablePlotsForCorrectPairing(iEvt, plottingData, [jetVectorDict[matchedJet[0]] for matchedJet in matchedQuarksToJets.values()], iAlgorithm)

        # ** B. Pick two jet pairs based on algorithm
        jetPair1, jetPair2, pairingMetric = selectPairsViaMatchingAlgorithm(plottingData, jetVectorDict, iAlgorithm)
    
        # ** C. Evaluate efficiency of pairing algorithm
        if thisEventIsMatchable:
            evaluatePairingEfficiency(eventCounterDict, matchedQuarksToJets, jetPair1, jetPair2, nJets, nBTags, iAlgorithm)
    
        # ** D. Calculate and save variables for BDT training for single algorithm set by saveAlgorithm
        if iAlgorithm == saveAlgorithm: 
            variablesForBDT = calculateVariablesForBDT(jetPair1, jetPair2, jetVectorDict, nJets, nBTags, 
                                                        l_missingET_met[iEvt], l_missingET_phi[iEvt], l_scalarHT[iEvt])
            outputDataForLearning.append(variablesForBDT)
"""
