#ifndef __L1Analysis_L1AnalysisEventDataFormat_H__
#define __L1Analysis_L1AnalysisEventDataFormat_H__

//-------------------------------------------------------------------------------
// Created 15/04/2010 - E. Conte, A.C. Le Bihan
// 
// 
// Original code : L1TriggerDPG/L1Ntuples/L1NtupleProducer
//-------------------------------------------------------------------------------

// #include <inttypes.h>
#include <TROOT.h>
#include <vector>
#include <TString.h>

namespace L1Analysis
{
  struct L1AnalysisEventDataFormat
  {
    L1AnalysisEventDataFormat() {Reset();}
    ~L1AnalysisEventDataFormat(){}
    
    void Reset()
    {  
       run = -1;
       event = -1;
       lumi = -1;
       bx = -1;
       orbit = 0;
       time = 0;
       hlt.resize(0);
    }

    int             run;
    int             event;
    int             lumi;
    int             bx;
    //boost::uint64_t orbit;
    ULong64_t orbit;
    //boost::uint64_t time;
    ULong64_t time;
    std::vector<TString> hlt;

    double puWeight;
    double nPV;
    
  }; 
}
#endif


