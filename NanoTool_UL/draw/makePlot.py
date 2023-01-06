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

from drawDiagnostics import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	ifile1 = "./fitDiagnosticsTest.root"
	name = "sig25_corr_veryhigh_btag_10"
	RData = drawDiagnostic(name, ifile1)
	print("draw Diagnositcs Finished")
