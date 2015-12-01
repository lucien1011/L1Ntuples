import FWCore.ParameterSet.Config as cms

# make L1 ntuples from RAW+RECO

process = cms.Process("L1NTUPLE")

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/SimL1Emulator_cff')
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load("JetMETCorrections.Configuration.DefaultJEC_cff")
## process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('RecoMET.METProducers.hcalnoiseinfoproducer_cfi')
process.load("CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi")

# output file
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('L1Tree.root')
)

# L1 raw to digi options
process.gctDigis.numberOfGctSamplesToUnpack = cms.uint32(5)
process.l1extraParticles.centralBxOnly = cms.bool(False)

# L1 ntuple producers
## process.load("L1TriggerDPG.L1Ntuples.l1NtupleProducer_cfi")
import L1TriggerDPG.L1Ntuples.l1NtupleProducer_cfi 
process.l1NtupleProducer = L1TriggerDPG.L1Ntuples.l1NtupleProducer_cfi.l1NtupleProducer.clone()

import L1TriggerDPG.L1Ntuples.l1NtupleProducer_Stage1Layer2_cfi 
process.l1NtupleProducerStage1Layer2 = L1TriggerDPG.L1Ntuples.l1NtupleProducer_Stage1Layer2_cfi.l1NtupleProducer.clone()

process.load("L1TriggerDPG.L1Ntuples.l1RecoTreeProducer_cfi")
process.load("L1TriggerDPG.L1Ntuples.l1ExtraTreeProducer_cfi")
process.load("L1TriggerDPG.L1Ntuples.l1MenuTreeProducer_cfi")
process.load("L1TriggerDPG.L1Ntuples.l1MuonRecoTreeProducer_cfi")
process.load("EventFilter.L1GlobalTriggerRawToDigi.l1GtTriggerMenuLite_cfi")

# Noise Filter
process.hcalnoise.fillCaloTowers = cms.bool(False)
process.hcalnoise.fillTracks = cms.bool(False)
process.ApplyBaselineHBHENoiseFilter = cms.EDFilter('BooleanFlagFilter',
			inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
			reverseDecision = cms.bool(False)
			)
process.ApplyHBHEIsoNoiseFilter = cms.EDFilter('BooleanFlagFilter',
		    inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHEIsoNoiseFilterResult'),
		        reverseDecision = cms.bool(False)
			)

process.hcalnoise.recHitCollName = cms.string("hbheprereco")

process.HBHENoiseFilterResultProducer.IgnoreTS4TS5ifJetInLowBVRegion = cms.bool(False) 
process.HBHENoiseFilterResultProducer.defaultDecision = cms.string("HBHENoiseFilterResultRun2Loose")

process.HBHENoiseFilterResultProducer.minZeros = cms.int32(9999)

process.p = cms.Path(
    process.RawToDigi
    +process.hcalLocalRecoSequence
    +process.hcalnoise
    +process.HBHENoiseFilterResultProducer
    +process.ApplyBaselineHBHENoiseFilter
    +process.ApplyHBHEIsoNoiseFilter
    +process.l1NtupleProducer
    +process.l1extraParticles
    +process.l1ExtraTreeProducer
    +process.l1GtTriggerMenuLite
    +process.l1MenuTreeProducer
    +process.l1RecoTreeProducer
    +process.l1MuonRecoTreeProducer
)

# job options
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
## process.GlobalTag.globaltag = 'GR_R_52_V7::All'
process.GlobalTag.globaltag = 'GR_R_52_V7'

SkipEvent = cms.untracked.vstring('ProductNotFound')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()
process.source = cms.Source ("PoolSource",
                             fileNames = readFiles,
                             secondaryFileNames = secFiles
                             )
