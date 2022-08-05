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

from applyTF import *

#from future import division

if __name__ == "__main__":
	print("Starting Run")
	bfile1 = "./FitHist.root"
	bfile2 = "./TF_Data.root"
	name = "FitTest"
	RData = Build(name, bfile1, bfile2)
	print("FitTest Finished")
