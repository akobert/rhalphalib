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


#from __future__ import print_function, division
import rhalphalib as rl
import numpy as np
import scipy.stats
import pickle
rl.util.install_roofit_helpers()
rl.ParametericSample.PreferRooParametricHist = False
import pandas as pd
import json


#from future import division

def GetBinX(hist, x):
	nbins = hist.GetNbinsX()
	lo = hist.GetXaxis().GetXmin() 
	hi = hist.GetXaxis().GetXmax()
	width = (hi-lo)/nbins

	return int((x-lo)/width) + 1
def GetBinY(hist, y):
	nbins = hist.GetNbinsY()
	lo = hist.GetYaxis().GetXmin() 
	hi = hist.GetYaxis().GetXmax()
	width = (hi-lo)/nbins

	return int((y-lo)/width) + 1
	

class Build:
	def __init__(self, name, ifile1):
		gROOT.SetBatch(True)
		gStyle.SetOptStat(0)



		#background files
		self.f = TFile.Open(ifile1, "READ")
		self.f.ls();

		self.tot_data = TH1F("tot_data", "Total Data", 100, 0, 220)
		self.tot_fit = TH1F("tot_fit", "Total Fit", 100, 0, 220)
		
		for i in range(0, 38):
			print("Bin"+str(i))

			fname = "ptbin"+str(i)+"pass_msd_fit_b"
			self.ptbin = self.f.Get(fname)	
			
			self.dataGraph = self.ptbin.getObject(0)
			self.fitGraph = self.ptbin.getObject(1)

#			print(type(self.dataGraph))
#			print(type(self.fitGraph))

#			self.data = TH1F("data", "Data", 40, 0, 200)
#			self.fit = TH1F("fit", "Fit", 40, 0, 200)

			self.data = self.dataGraph.GetHistogram()
#			self.fit = self.fitGraph.GetHistogram()

#			for j in range(0,41):
#				x=0
#				y=0
#				x = self.dataGraph.GetPointX(j)
#				y = self.dataGraph.GetPointY(j)
#				self.data.Fill(x,y)
#				x = self.fitGraph.GetPointX(j)
#				y = self.fitGraph.GetPointY(j)
#				self.fit.Fill(x,y)
				
			self.tot_data.Add(self.data)
#			self.tot_fit.Add(self.fit)
			
			
		
		c1 = TCanvas()
		c1.cd()
		l1 = TLegend(.6, .75, .9, .9)
		self.tot_data.Draw("hist")
		self.tot_fit.Draw("same hist")
		l1.AddEntry(self.tot_data, "Data")
#		l1.AddEntry(self.tot_fit, "Fit")
		l1.Draw()
		c1.SaveAs("./Total_FitPlot_v2.png")



