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
	def __init__(self, name, bfile1, bfile2, bfile3, dfile1, sfile1, sfile2, sfile3, sfile4, sfile5, sfile6, sfile7, sfile8):
		gROOT.SetBatch(True)

		#Output Files
	        ofile = ROOT.TFile(name + ".root", "RECREATE")
	        ofile.cd()


		#background files
		self.f = TFile.Open(dfile1, "READ")
		self.f.ls();

		self.Data_p1 = self.f.Get("pass_soft")
		self.Data_p2 = self.f.Get("pass_photon_pt")
		self.Data_p3 = self.f.Get("pass_jet_pt")
		self.Data_p4 = self.f.Get("pass_rho")
		self.Data_p5 = self.f.Get("pass_photon_eta")
		self.Data_p6 = self.f.Get("pass_jet_eta")
		self.Data_p7 = self.f.Get("jet_pt_soft_pass")
		self.Data_p7_1 = self.f.Get("jet_pt_soft_pass")
		self.Data_p7_w = self.f.Get("jet_pt_soft_pass_wide")
		self.Data_p9 = self.f.Get("jet_pt_rho_pass")
		self.Data_f1 = self.f.Get("fail_soft")
		self.Data_f2 = self.f.Get("fail_photon_pt")
		self.Data_f3 = self.f.Get("fail_jet_pt")
		self.Data_f4 = self.f.Get("fail_rho")
		self.Data_f5 = self.f.Get("fail_photon_eta")
		self.Data_f6 = self.f.Get("fail_jet_eta")
		self.Data_f7 = self.f.Get("jet_pt_soft_fail")
		self.Data_f7_1 = self.f.Get("jet_pt_soft_fail")
		self.Data_f7_w = self.f.Get("jet_pt_soft_fail_wide")
		self.Data_f9 = self.f.Get("jet_pt_rho_fail")
		self.Data_h1 = self.f.Get("softdrop")
		self.Data_h2 = self.f.Get("N2")
		self.Data_h4 = self.f.Get("photon_pt")
		self.Data_h5 = self.f.Get("jet_pt")
		self.Data_h6 = self.f.Get("jet_eta")
		self.Data_h7 = self.f.Get("fine_rho")
		self.Data_h8 = self.f.Get("photon_eta")

		self.g = TFile(bfile3, "READ")
		self.TTBar_p1 = self.g.Get("pass_soft")
		self.TTBar_p2 = self.g.Get("pass_photon_pt")
		self.TTBar_p3 = self.g.Get("pass_jet_pt")
		self.TTBar_p4 = self.g.Get("pass_rho")
		self.TTBar_p5 = self.g.Get("pass_photon_eta")
		self.TTBar_p6 = self.g.Get("pass_jet_eta")
		self.TTBar_p7 = self.g.Get("jet_pt_soft_pass")
		self.TTBar_p7_w = self.g.Get("jet_pt_soft_pass_wide")
		self.TTBar_f1 = self.g.Get("fail_soft")
		self.TTBar_f2 = self.g.Get("fail_photon_pt")
		self.TTBar_f3 = self.g.Get("fail_jet_pt")
		self.TTBar_f4 = self.g.Get("fail_rho")
		self.TTBar_f5 = self.g.Get("fail_photon_eta")
		self.TTBar_f6 = self.g.Get("fail_jet_eta")
		self.TTBar_f7 = self.g.Get("jet_pt_soft_fail")
		self.TTBar_f7_w = self.g.Get("jet_pt_soft_fail_wide")
		self.TTBar_h1 = self.g.Get("softdrop")
		self.TTBar_h2 = self.g.Get("N2")

		self.s1 = TFile(sfile1, "READ")
		self.sig1_p7 = self.s1.Get("jet_pt_soft_pass")
		self.sig1_f7 = self.s1.Get("jet_pt_soft_fail")
		self.sig1_p7_w = self.s1.Get("jet_pt_soft_pass_wide")
		self.sig1_f7_w = self.s1.Get("jet_pt_soft_fail_wide")
		
		self.s2 = TFile(sfile2, "READ")
		self.sig2_p7 = self.s2.Get("jet_pt_soft_pass")
		self.sig2_f7 = self.s2.Get("jet_pt_soft_fail")
		self.sig2_p7_w = self.s2.Get("jet_pt_soft_pass_wide")
		self.sig2_f7_w = self.s2.Get("jet_pt_soft_fail_wide")
		
		self.s3 = TFile(sfile3, "READ")
		self.sig3_p7 = self.s3.Get("jet_pt_soft_pass")
		self.sig3_f7 = self.s3.Get("jet_pt_soft_fail")
		self.sig3_p7_w = self.s3.Get("jet_pt_soft_pass_wide")
		self.sig3_f7_w = self.s3.Get("jet_pt_soft_fail_wide")
		
		self.s4 = TFile(sfile4, "READ")
		self.sig4_p7 = self.s4.Get("jet_pt_soft_pass")
		self.sig4_f7 = self.s4.Get("jet_pt_soft_fail")
		self.sig4_p7_w = self.s4.Get("jet_pt_soft_pass_wide")
		self.sig4_f7_w = self.s4.Get("jet_pt_soft_fail_wide")
		
		self.s5 = TFile(sfile5, "READ")
		self.sig5_p7 = self.s5.Get("jet_pt_soft_pass")
		self.sig5_f7 = self.s5.Get("jet_pt_soft_fail")
		self.sig5_p7_w = self.s5.Get("jet_pt_soft_pass_wide")
		self.sig5_f7_w = self.s5.Get("jet_pt_soft_fail_wide")
		
		self.s6 = TFile(sfile6, "READ")
		self.sig6_p7 = self.s6.Get("jet_pt_soft_pass")
		self.sig6_f7 = self.s6.Get("jet_pt_soft_fail")
		self.sig6_p7_w = self.s6.Get("jet_pt_soft_pass_wide")
		self.sig6_f7_w = self.s6.Get("jet_pt_soft_fail_wide")
		
		self.s7 = TFile(sfile7, "READ")
		self.sig7_p7 = self.s7.Get("jet_pt_soft_pass")
		self.sig7_f7 = self.s7.Get("jet_pt_soft_fail")
		self.sig7_p7_w = self.s7.Get("jet_pt_soft_pass_wide")
		self.sig7_f7_w = self.s7.Get("jet_pt_soft_fail_wide")
		
		self.s8 = TFile(sfile8, "READ")
		self.sig8_p7 = self.s8.Get("jet_pt_soft_pass")
		self.sig8_f7 = self.s8.Get("jet_pt_soft_fail")
		self.sig8_p7_w = self.s8.Get("jet_pt_soft_pass_wide")
		self.sig8_f7_w = self.s8.Get("jet_pt_soft_fail_wide")


	
		#currently using 10% of data	

		self.TTBar_p1.Scale(.1)
		self.TTBar_p2.Scale(.1)
		self.TTBar_p3.Scale(.1)
		self.TTBar_p4.Scale(.1)
		self.TTBar_p5.Scale(.1)
		self.TTBar_p6.Scale(.1)
		self.TTBar_p7.Scale(.1)
		self.TTBar_p7_w.Scale(.1)
		self.TTBar_f1.Scale(.1)
		self.TTBar_f2.Scale(.1)
		self.TTBar_f3.Scale(.1)
		self.TTBar_f4.Scale(.1)
		self.TTBar_f5.Scale(.1)
		self.TTBar_f6.Scale(.1)
		self.TTBar_f7.Scale(.1)
		self.TTBar_f7_w.Scale(.1)
		self.TTBar_h1.Scale(.1)
		self.TTBar_h2.Scale(.1)

		self.sig1_p7.Scale(.1)
		self.sig1_f7.Scale(.1)
		self.sig1_p7_w.Scale(.1)
		self.sig1_f7_w.Scale(.1)
		self.sig2_p7.Scale(.1)
		self.sig2_f7.Scale(.1)
		self.sig2_p7_w.Scale(.1)
		self.sig2_f7_w.Scale(.1)
		self.sig3_p7.Scale(.1)
		self.sig3_f7.Scale(.1)
		self.sig3_p7_w.Scale(.1)
		self.sig3_f7_w.Scale(.1)
		self.sig4_p7.Scale(.1)
		self.sig4_f7.Scale(.1)
		self.sig4_p7_w.Scale(.1)
		self.sig4_f7_w.Scale(.1)
		self.sig5_p7.Scale(.1)
		self.sig5_f7.Scale(.1)
		self.sig5_p7_w.Scale(.1)
		self.sig5_f7_w.Scale(.1)
		self.sig6_p7.Scale(.1)
		self.sig6_f7.Scale(.1)
		self.sig6_p7_w.Scale(.1)
		self.sig6_f7_w.Scale(.1)
		self.sig7_p7.Scale(.1)
		self.sig7_f7.Scale(.1)
		self.sig7_p7_w.Scale(.1)
		self.sig7_f7_w.Scale(.1)
		self.sig8_p7.Scale(.1)
		self.sig8_f7.Scale(.1)
		self.sig8_p7_w.Scale(.1)
		self.sig8_f7_w.Scale(.1)

		#Make Coarse bin versions of jet_pt_soft pass/fail
#		self.Data_p7_1.Rebin2D(2,1)
#		self.Data_f7_1.Rebin2D(2,1)
		
#		self.Data_p9.Rebin2D(2,1)
#		self.Data_f9.Rebin2D(2,1)
	
		self.Data_p9.SetAxisRange(-7., -2., "Y")
		self.Data_f9.SetAxisRange(-7., -2., "Y")
		#self.TTBar_p9.SetAxisRange(-7., -2., "Y")
		#self.TTBar_f9.SetAxisRange(-7., -2., "Y")
	
		
		ofile.WriteObject(self.Data_p1, "Data_pass_soft")
		ofile.WriteObject(self.Data_p2, "Data_pass_pho_pt")
		ofile.WriteObject(self.Data_p3, "Data_pass_jet_pt")
		ofile.WriteObject(self.Data_p4, "Data_pass_rho")
		ofile.WriteObject(self.Data_p5, "Data_pass_pho_eta")
		ofile.WriteObject(self.Data_p6, "Data_pass_jet_eta")
		ofile.WriteObject(self.Data_p7, "Data_pass_jet_pt_soft")
		ofile.WriteObject(self.Data_p7_1, "Data_pass_jet_pt_soft_coarse")
		ofile.WriteObject(self.Data_p7_w, "Data_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.Data_p9, "Data_pass_jet_pt_rho")
		ofile.WriteObject(self.Data_f1, "Data_fail_soft")
		ofile.WriteObject(self.Data_f2, "Data_fail_pho_pt")
		ofile.WriteObject(self.Data_f3, "Data_fail_jet_pt")
		ofile.WriteObject(self.Data_f4, "Data_fail_rho")
		ofile.WriteObject(self.Data_f5, "Data_fail_pho_eta")
		ofile.WriteObject(self.Data_f6, "Data_fail_jet_eta")
		ofile.WriteObject(self.Data_f7, "Data_fail_jet_pt_soft")
		ofile.WriteObject(self.Data_f7_1, "Data_fail_jet_pt_soft_coarse")
		ofile.WriteObject(self.Data_f7_w, "Data_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.Data_f9, "Data_fail_jet_pt_rho")
		ofile.WriteObject(self.Data_h1, "Data_soft")
		ofile.WriteObject(self.Data_h2, "Data_N2")
		ofile.WriteObject(self.Data_h4, "Data_pho_pt")
		ofile.WriteObject(self.Data_h5, "Data_jet_pt")
		ofile.WriteObject(self.Data_h6, "Data_jet_eta")
		ofile.WriteObject(self.Data_h7, "Data_rho")
		ofile.WriteObject(self.Data_h8, "Data_pho_eta")
		
		ofile.WriteObject(self.TTBar_p1, "TTBar_pass_soft")
		ofile.WriteObject(self.TTBar_p2, "TTBar_pass_pho_pt")
		ofile.WriteObject(self.TTBar_p3, "TTBar_pass_jet_pt")
		ofile.WriteObject(self.TTBar_p4, "TTBar_pass_rho")
		ofile.WriteObject(self.TTBar_p5, "TTBar_pass_pho_eta")
		ofile.WriteObject(self.TTBar_p6, "TTBar_pass_jet_eta")
		ofile.WriteObject(self.TTBar_p7, "TTBar_pass_jet_pt_soft")
		ofile.WriteObject(self.TTBar_p7_w, "TTBar_pass_jet_pt_soft_wide")
	#	ofile.WriteObject(self.TTBar_p9, "TTBar_pass_jet_pt_rho")
		ofile.WriteObject(self.TTBar_f1, "TTBar_fail_soft")
		ofile.WriteObject(self.TTBar_f2, "TTBar_fail_pho_pt")
		ofile.WriteObject(self.TTBar_f3, "TTBar_fail_jet_pt")
		ofile.WriteObject(self.TTBar_f4, "TTBar_fail_rho")
		ofile.WriteObject(self.TTBar_f5, "TTBar_fail_pho_eta")
		ofile.WriteObject(self.TTBar_f6, "TTBar_fail_jet_eta")
		ofile.WriteObject(self.TTBar_f7, "TTBar_fail_jet_pt_soft")
		ofile.WriteObject(self.TTBar_f7_w, "TTBar_fail_jet_pt_soft_wide")
	#	ofile.WriteObject(self.TTBar_f9, "TTBar_fail_jet_pt_rho")
		ofile.WriteObject(self.TTBar_h1, "TTBar_soft")
		ofile.WriteObject(self.TTBar_h2, "TTBar_N2")
		#ofile.WriteObject(self.TTBar_h4, "TTBar_pho_pt")
		#ofile.WriteObject(self.TTBar_h5, "TTBar_jet_pt")
		#ofile.WriteObject(self.TTBar_h6, "TTBar_jet_eta")
		#ofile.WriteObject(self.TTBar_h7, "TTBar_rho")
		#ofile.WriteObject(self.TTBar_h8, "TTBar_pho_eta")
		
		ofile.WriteObject(self.sig1_p7, "Sig10_pass_jet_pt_soft")
		ofile.WriteObject(self.sig1_f7, "Sig10_fail_jet_pt_soft")
		ofile.WriteObject(self.sig1_p7_w, "Sig10_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig1_f7_w, "Sig10_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig2_p7, "Sig20_pass_jet_pt_soft")
		ofile.WriteObject(self.sig2_f7, "Sig20_fail_jet_pt_soft")
		ofile.WriteObject(self.sig2_p7_w, "Sig20_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig2_f7_w, "Sig20_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig3_p7, "Sig25_pass_jet_pt_soft")
		ofile.WriteObject(self.sig3_f7, "Sig25_fail_jet_pt_soft")
		ofile.WriteObject(self.sig3_p7_w, "Sig25_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig3_f7_w, "Sig25_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig4_p7, "Sig50_pass_jet_pt_soft")
		ofile.WriteObject(self.sig4_f7, "Sig50_fail_jet_pt_soft")
		ofile.WriteObject(self.sig4_p7_w, "Sig50_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig4_f7_w, "Sig50_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig5_p7, "Sig75_pass_jet_pt_soft")
		ofile.WriteObject(self.sig5_f7, "Sig75_fail_jet_pt_soft")
		ofile.WriteObject(self.sig5_p7_w, "Sig75_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig5_f7_w, "Sig75_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig6_p7, "Sig100_pass_jet_pt_soft")
		ofile.WriteObject(self.sig6_f7, "Sig100_fail_jet_pt_soft")
		ofile.WriteObject(self.sig6_p7_w, "Sig100_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig6_f7_w, "Sig100_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig7_p7, "Sig125_pass_jet_pt_soft")
		ofile.WriteObject(self.sig7_f7, "Sig125_fail_jet_pt_soft")
		ofile.WriteObject(self.sig7_p7_w, "Sig125_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig7_f7_w, "Sig125_fail_jet_pt_soft_wide")
		ofile.WriteObject(self.sig8_p7, "Sig150_pass_jet_pt_soft")
		ofile.WriteObject(self.sig8_f7, "Sig150_fail_jet_pt_soft")
		ofile.WriteObject(self.sig8_p7_w, "Sig150_pass_jet_pt_soft_wide")
		ofile.WriteObject(self.sig8_f7_w, "Sig150_fail_jet_pt_soft_wide")
		

		ROOT.gInterpreter.Declare("Double_t widebins[9] = {0, 125, 135, 145, 160, 175, 200, 245, 2000};")
                h1 = TH2F("ratio", "Ratio of Pass/Fail Events in Jet pT vs. Softdrop Mass", 8, widebins, 40, 0, 200)

                for i in range(1, self.Data_p7_w.GetNbinsX()+1):
                        for j in range(1, self.Data_p7_w.GetNbinsY()+1):
                                rpass = self.Data_p7_w.GetBinContent(i,j) - self.TTBar_p7_w.GetBinContent(i,j)
                                rfail = self.Data_f7_w.GetBinContent(i,j) - self.TTBar_f7_w.GetBinContent(i,j)

                                if (rpass<=0 or rfail<=0) or (rpass/rfail)>=0.5:
                                        h1.SetBinContent(i,j,0)
                                else:
                                        h1.SetBinContent(i,j,rpass/rfail)
					print("Bin: "+str(i)+", "+str(j))
					print("Value: "+str(rpass/rfail))

                ofile.WriteObject(h1, "Ratio")
                ofile.Write()
