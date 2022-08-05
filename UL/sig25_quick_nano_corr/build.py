import ROOT
from ROOT import *
import os
from array import array
import math
from math import *
import sys
import glob
import csv
import ctypes
from ctypes import *
import XRootD
from pyxrootd import client
import numpy as np

from buildfile import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/NanoTool/corrected/RData_GJets_UL_20_quick_nano_corr.root"
	bfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/NanoTool/corrected/RData_TTBar_UL_20_quick_nano_corr.root"
	
	dfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/quick/NanoTool/corrected/RData_Data_UL_quick_nano_corr.root" 
	
	

	#Signal Files
	sfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_10GeV_20_nano_corr.root"
	sfile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_20GeV_20_nano_corr.root"
	sfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_25GeV_20_nano_corr.root"
	sfile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_50GeV_20_nano_corr.root"
	sfile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_75GeV_20_nano_corr.root"
	sfile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_100GeV_20_nano_corr.root"
	sfile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_125GeV_20_nano_corr.root"
	sfile8 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/signalMC/NanoTool/corrected/RData_150GeV_20_nano_corr.root"

	name = "FitHist"
	RData = Build(name, bfile1, bfile3, dfile1, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, sfile7, sfile8)
	print("FitHist Finished")
