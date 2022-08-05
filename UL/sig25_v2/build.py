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
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/RData_GJets_UL_20.root"
	bfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/RData_TTBar_UL_20.root"
	
	#Temporariliy using backup file
	dfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/RData_Data_UL.root" 
#	dfile1 = "./RData_Data_backup.root" 
	
	

	#Signal Files
	sfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_10GeV_UL_20.root"
	sfile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_20GeV_UL_20.root"
	sfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_25GeV_UL_20.root"
	sfile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_50GeV_UL_20.root"
	sfile5 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_75GeV_UL_20.root"
	sfile6 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_100GeV_UL_20.root"
	sfile7 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_125GeV_UL_20.root"
	sfile8 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/UL/signalMC/RData_150GeV_UL_20.root"

	name = "FitHist"
	RData = Build(name, bfile1, bfile3, dfile1, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, sfile7, sfile8)
	print("FitHist Finished")
