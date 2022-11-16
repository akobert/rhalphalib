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

#from future import division

class Build:
	def __init__(self, name, bfile1, bfile2, bfile3, bfile4, dfile1, sfile1):
		gROOT.SetBatch(True)

		#Output Files
	        ofile = ROOT.TFile(name + ".root", "RECREATE")
	        ofile.cd()


		#background files
		self.f = TFile.Open(dfile1, "READ")
		self.f.ls();

		self.Data_p7_w = self.f.Get("jet_pt_soft_pass_wide5")
		self.Data_f7_w = self.f.Get("jet_pt_soft_fail_wide5")
		self.Data_p1 = self.f.Get("pass_soft")	
		self.Data_f1 = self.f.Get("fail_soft")	

		self.g = TFile(bfile1, "READ")
		self.TTBar_p7_w = self.g.Get("jet_pt_soft_pass_wide5")
		self.TTBar_f7_w = self.g.Get("jet_pt_soft_fail_wide5")
		
		self.h = TFile(bfile2, "READ")
		self.wgamma_p7_w = self.h.Get("jet_pt_soft_pass_wide5")
		self.wgamma_f7_w = self.h.Get("jet_pt_soft_fail_wide5")
		
		self.j = TFile(bfile3, "READ")
		self.zgamma_p7_w = self.j.Get("jet_pt_soft_pass_wide5")
		self.zgamma_f7_w = self.j.Get("jet_pt_soft_fail_wide5")
		
		self.k = TFile(bfile4, "READ")
		self.GJ_p7_w = self.k.Get("jet_pt_soft_pass_wide5")
		self.GJ_f7_w = self.k.Get("jet_pt_soft_fail_wide5")

		self.s1 = TFile(sfile1, "READ")
		self.sig1_p7_w = self.s1.Get("jet_pt_soft_pass_wide5")
		self.sig1_f7_w = self.s1.Get("jet_pt_soft_fail_wide5")
		


	
		#currently using 10% of data
		#59.9 fb -> 5.9 (Scale by .1)

		#scaled in analysis code
		self.TTBar_p7_w.Scale(.1)
		self.TTBar_f7_w.Scale(.1)
		self.wgamma_p7_w.Scale(.1)
		self.wgamma_f7_w.Scale(.1)
		self.zgamma_p7_w.Scale(.1)
		self.zgamma_f7_w.Scale(.1)
		self.GJ_p7_w.Scale(.1)
		self.GJ_f7_w.Scale(.1)
		self.sig1_p7_w.Scale(.1)
		self.sig1_f7_w.Scale(.1)

		


	
		
		ofile.WriteObject(self.Data_p7_w, "Data_pass_jet_pt_soft_wide5")
		ofile.WriteObject(self.Data_f7_w, "Data_fail_jet_pt_soft_wide5")
		ofile.WriteObject(self.Data_p1, "Data_pass_soft")
		ofile.WriteObject(self.Data_f1, "Data_fail_soft")
		
		
		ofile.WriteObject(self.TTBar_p7_w, "TTBar_pass_jet_pt_soft_wide5")
		ofile.WriteObject(self.TTBar_f7_w, "TTBar_fail_jet_pt_soft_wide5")
		ofile.WriteObject(self.wgamma_p7_w, "WGamma_pass_jet_pt_soft_wide5")
		ofile.WriteObject(self.wgamma_f7_w, "WGamma_fail_jet_pt_soft_wide5")
		ofile.WriteObject(self.zgamma_p7_w, "ZGamma_pass_jet_pt_soft_wide5")
		ofile.WriteObject(self.zgamma_f7_w, "ZGamma_fail_jet_pt_soft_wide5")
		ofile.WriteObject(self.GJ_p7_w, "GJ_pass_jet_pt_soft_wide5")
		ofile.WriteObject(self.GJ_f7_w, "GJ_fail_jet_pt_soft_wide5")
		
		ofile.WriteObject(self.sig1_p7_w, "Sig25_pass_jet_pt_soft_wide5")
		ofile.WriteObject(self.sig1_f7_w, "Sig25_fail_jet_pt_soft_wide5")
		

                ofile.Write()
