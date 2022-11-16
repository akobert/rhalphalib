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
	bfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/TTBar_UL_nano_merged.root"
	bfile2 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/WGamma_UL_nano_merged.root"
	bfile3 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/ZGamma_UL_nano_merged.root"
	bfile4 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/GJ_UL.root"
	
	dfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/Data_UL.root" 
	
	

	#Signal Files
	sfile1 = "/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL_corr_btag/M25_UL_nano_merged.root"
	
	name = "FitHist"
	RData = Build(name, bfile1, bfile2, bfile3, bfile4, dfile1, sfile1)
	print("FitHist Finished")
