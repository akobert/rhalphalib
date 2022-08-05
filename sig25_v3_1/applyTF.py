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
	def __init__(self, name, bfile1, bfile2):
		gROOT.SetBatch(True)
		gStyle.SetOptStat(0)

		PF = 0.27097030473519085

		#Output Files
	        ofile = ROOT.TFile(name + ".root", "RECREATE")
	        ofile.cd()


		#background files
		self.f = TFile.Open(bfile1, "READ")
		self.f.ls();

		self.Data_p7 = self.f.Get("Data_pass_jet_pt_soft_coarse")
		self.Data_p9 = self.f.Get("Data_pass_jet_pt_rho")
		self.Data_f7 = self.f.Get("Data_fail_jet_pt_soft_coarse")
		self.Data_f9 = self.f.Get("Data_fail_jet_pt_rho")
		

		self.g = TFile.Open(bfile2, "READ")
		self.g.ls();
		self.Data_rpt = self.g.Get("rpt_TF")
		self.Data_mpt = self.g.Get("mpt_TF")
		
		self.Data_rpt2 = TH2F("rpt_TF2", "Jet pT vs. Rho TF", 40, 0, 2000, 40, -7, -2)
		self.Data_rpt2.SetXTitle("Jet pT")
		self.Data_rpt2.SetYTitle("Rho")
		for i in range(1, self.Data_rpt2.GetNbinsX()+1):
			for j in range(1, self.Data_rpt2.GetNbinsY()+1):
				self.Data_rpt2.SetBinContent(i, j, self.Data_rpt.GetBinContent(j, i))
	
#                rho_bern = TF2("rho_pt_bern", "0.9727 + 0.9738 * (x/2000.0) + 1.0336 * (x/2000.0)^2 + 1.11796* ((y + 7.0)/5.0) + 0.9591 * (x/2000.0)*((y + 7.0)/5.0) + 0.8658 * ((y + 7.0)/5.0)^2 * (x/2000.0) + 0.8985 * (x/2000.0)^2 + 0.7481 * ((y + 7.0)/5.0) * (x/2000.0)^2 + 1.251 * (x/2000.0)^2 * ((y + 7.0)/5.0)^2", 0, 2000, -7, -2)
#		ofile.WriteObject(rho_bern, "rho_bern")


		#Bernstein Polynomial evaluation
		final_vals = np.genfromtxt('final_vals.csv')
		final_vals = final_vals.reshape(3,3)

		tf_MCtempl = rl.BernsteinPoly('tf_MCtempl', (2, 2), ['pt', 'rho'], init_params=final_vals, limits=(-10, 10))
		
		msdbins = np.linspace(0, 200, 41)
		pts = np.linspace(0,2000,21)
		ptpts, msdpts = np.meshgrid(pts[:-1] + 0.5 * np.diff(pts), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
		ptpts_scaled = (ptpts) / (2000.)
		rhopts = 2*np.log(msdpts/ptpts)
		rhopts_scaled = (rhopts - (-7.)) / ((-2.0) - (-7.))
	
		validbins = (rhopts_scaled >= 0) & (rhopts_scaled <= 1)

    		ptpts = ptpts[validbins]
    		msdpts = msdpts[validbins]
    		ptpts_scaled = ptpts_scaled[validbins]
    		rhopts_scaled = rhopts_scaled[validbins]
	
		tf_MCtempl_vals = tf_MCtempl(ptpts_scaled, rhopts_scaled, nominal=True)
    		df = pd.DataFrame([])
    		df['msd'] = msdpts.reshape(-1)
    		df['pt'] = ptpts.reshape(-1)
    		df['MCTF'] = tf_MCtempl_vals.reshape(-1)

    		mpt = df.to_numpy()
		mpt_TF_test = TH2F("mpt_TF_test", "Mass vs. pT Transfer Factor", 40, 0, 200, 40, 0, 2000)
		for i in range(0, mpt.shape[0]):
        		mpt_TF_test.Fill(mpt[i][0], mpt[i][1], mpt[i][2])
#       		print(mpt[i][2])

		ofile.WriteObject(mpt_TF_test, "mpt_TF_test")

		rhos = np.linspace(-7.0,-2.0,21)
    		ptpts, rhopts = np.meshgrid(pts[:-1] + 0.5*np.diff(pts), rhos[:-1] + 0.5 * np.diff(rhos), indexing='ij')
    		ptpts_scaled = (ptpts) / (2000)
   		rhopts_scaled = (rhopts - (-7.0)) / ((-2.0) - (-7.0))
    		validbins = (rhopts_scaled >= 0) & (rhopts_scaled <= 1)

    		ptpts = ptpts[validbins]
    		rhopts = rhopts[validbins]
    		ptpts_scaled = ptpts_scaled[validbins]
    		rhopts_scaled = rhopts_scaled[validbins]

    		tf_MCtempl_vals = tf_MCtempl(ptpts_scaled, rhopts_scaled, nominal=True)

    		df = pd.DataFrame([])
    		df['rho'] = rhopts.reshape(-1)
    		df['pt'] = ptpts.reshape(-1)
    		df['MCTF'] = tf_MCtempl_vals.reshape(-1)

    		rpt = df.to_numpy()

    		rpt_TF_test = TH2F("rpt_TF_test", "Rho vs. pT Transfer Factor", 40, -7, -2, 40, 0, 2000)
    		for i in range(0, rpt.shape[0]):
        		rpt_TF_test.Fill(rpt[i][0], rpt[i][1], rpt[i][2])


    		ofile.WriteObject(rpt_TF_test, "rpt_TF_test")

		
		
	
		self.Data_mpt2 = TH2F("mpt_TF2", "Jet pT vs. msd TF", 40, 0, 2000, 40, 0, 200)
		self.Data_mpt2.SetXTitle("Jet pT")
		self.Data_mpt2.SetYTitle("msd")
		for i in range(1, self.Data_mpt2.GetNbinsX()+1):
			for j in range(1, self.Data_mpt2.GetNbinsY()+1):
				self.Data_mpt2.SetBinContent(i, j, self.Data_mpt.GetBinContent(j, i))
		
#		self.Data_rpt2.SetAxisRange(0.75, 1.25, "Z")
#		self.Data_mpt2.SetAxisRange(0.75, 1.25, "Z")
		
		ofile.WriteObject(self.Data_rpt2, "rpt2_TF")
		ofile.WriteObject(self.Data_mpt2, "mpt2_TF")

	
		self.back_est_msd = TH2F("back_est_msd", "MSD Background Estimate (P/F * TF * Fail)", 40, 0, 2000, 40, 0, 200)
		self.back_est_msd.SetXTitle("Jet pT")
		self.back_est_msd.SetYTitle("msd")
		for i in range(1, self.back_est_msd.GetNbinsX()+1):
			for j in range(1, self.back_est_msd.GetNbinsY()+1):
				fail_mpt = self.Data_f7.GetBinContent(i,j)
				TF = self.Data_mpt2.GetBinContent(i,j)
				self.back_est_msd.SetBinContent(i, j, PF*TF*fail_mpt)
		




		self.back_est_rho = TH2F("back_est_rho", "Rho Background Estimate (P/F * TF * Fail)", 40, 0, 2000, 40, -7, -2)
		self.back_est_rho.SetXTitle("Jet pT")
		self.back_est_rho.SetYTitle("rho")

		for i in range(1, self.back_est_rho.GetNbinsX()+1):
			for j in range(1, self.back_est_rho.GetNbinsY()+1):
				fail_rpt = self.Data_f9.GetBinContent(i,j+4) #+4 because of different min
				TF = self.Data_rpt2.GetBinContent(i,j)
				self.back_est_rho.SetBinContent(i, j, PF*TF*fail_rpt)
		


#		self.back_est_rho2 = TH2F("back_est_rho2", "Rho Background Estimate2 (P/F * TF * Fail)", 20, 0, 2000, 20, -7, -2)
#		self.back_est_rho2.SetXTitle("Jet pT")
#		self.back_est_rho2.SetYTitle("rho")

#		for i in range(1, self.back_est_rho2.GetNbinsX()+1):
#			for j in range(1, self.back_est_rho2.GetNbinsY()+1):
#				fail_rpt = self.Data_f9.GetBinContent(i,j+4) #+4 because of different min
#				xval = self.back_est_rho2.GetXaxis().GetBinCenter(i)
#				yval = self.back_est_rho2.GetYaxis().GetBinCenter(j)
#				print("xval: "+str(xval)+" yval: "+str(yval))
#				TF = rho_bern(xval, yval)
#				print("TF: "+str(TF))
#				self.back_est_rho.SetBinContent(i, j, PF*TF*fail_rpt)

		
		c1 = TCanvas()
	#	c1.cd()
		a = 0
		b = 50
		l1 = TLegend(.6, .75, .9, .9)

                self.zero = TH1F("zero", "zero line", 40, 0, 200)
                self.zero.SetLineColor(kBlack)

                for z in range(1, self.zero.GetNbinsX()+1):
                        self.zero.SetBinContent(z, 0)

		self.jpt_soft_pass_total = TH1F("jsp_total", "Softdrop Mass Sum of pT Slices", 40, 0, 200)
		self.jpt_soft_pass_total_est = TH1F("jsp_total_est", "Softdrop Mass Sum of pT Slices", 40, 0, 200)
		self.jpt_soft_pass_total_est.SetLineColor(kRed)
	
		self.jpt_pull = TH1F("jpt_pull", "", 40, 0, 200)
		self.jpt_pull.SetTitle(";Softdrop Mass;#frac{Data-Background}{#sigma_{Data}};")
		self.jpt_pull.SetTitleSize(0.065, "y")	
		self.jpt_pull.SetAxisRange(-13,13,"Y")	
		for i in range(1, self.back_est_msd.GetNbinsX()+1):
			c1.Clear()
	#		c1.Divide(1,2)
			pad1 = TPad("pad1", "50%", 0.0, 0.5, 1.0, 1.0)
			pad2 = TPad("pad2", "50%", 0.0, 0.0, 1.0, 0.5)
			pad1.Draw()
			pad2.Draw()

			l1.Clear()
			pad1.cd()
			self.jpt_soft_pass_slice = self.Data_p7.ProjectionY("jpt_soft", i, i)
			self.jpt_soft_pass_slice_est = self.back_est_msd.ProjectionY("jpt_soft_est", i, i)
			
			self.jpt_soft_pass_total.Add(self.jpt_soft_pass_slice)
			self.jpt_soft_pass_total_est.Add(self.jpt_soft_pass_slice_est)

			self.jpt_soft_pass_slice.SetTitle("Softdrop Mass in pT slice "+str(a)+"-"+str(b))
			self.jpt_soft_pass_slice_est.SetLineColor(kRed)
			self.jpt_soft_pass_slice.Draw("histe")
			self.jpt_soft_pass_slice_est.Draw("same hist")
			l1.AddEntry(self.jpt_soft_pass_slice, "Passing Events")
			l1.AddEntry(self.jpt_soft_pass_slice_est, "Background Estimation")
			l1.Draw()
			
			pad2.cd()
			self.jpt_pull.Reset()
			for j in range(1, self.jpt_soft_pass_slice.GetNbinsX()+1):
				if self.jpt_soft_pass_slice.GetBinContent(j) != 0 and self.jpt_soft_pass_slice_est.GetBinContent(j) != 0:
					pull = (self.jpt_soft_pass_slice.GetBinContent(j) - self.jpt_soft_pass_slice_est.GetBinContent(j))/self.jpt_soft_pass_slice.GetBinError(j)
					if i == 3 or i == 2 or i==4:
                               		 	print(self.jpt_soft_pass_slice_est.GetBinContent(j))
						print(pull)
					self.jpt_pull.SetBinContent(j, pull)

			self.jpt_pull.Draw("")
			pad2.SetGridy()
			self.zero.Draw("same hist")			

			c1.SaveAs("./ptslices/msd_datafine_slice_"+str(a)+"_"+str(b)+".png")
			a += 50
			b += 50
		
		c1.Clear()
		pad1 = TPad("pad1", "50%", 0.0, 0.5, 1.0, 1.0)
		pad2 = TPad("pad2", "50%", 0.0, 0.0, 1.0, 0.5)
		pad1.Draw()
		pad2.Draw()
		l1.Clear()
		pad1.cd()
		self.jpt_soft_pass_total.Draw("histe")
		self.jpt_soft_pass_total_est.Draw("same hist")
		l1.AddEntry(self.jpt_soft_pass_total, "Passing Events")
		l1.AddEntry(self.jpt_soft_pass_total_est, "Background Estimation")
		l1.Draw()
		
		pad2.cd()
		self.jpt_pull.Reset()
		self.jpt_pull.SetAxisRange(-30,30,"Y")	
		for j in range(1, self.jpt_soft_pass_total.GetNbinsX()+1):
			if self.jpt_soft_pass_total.GetBinContent(j) != 0 and self.jpt_soft_pass_total_est.GetBinContent(j) != 0:
				pull = (self.jpt_soft_pass_total.GetBinContent(j) - self.jpt_soft_pass_total_est.GetBinContent(j))/self.jpt_soft_pass_total.GetBinError(j)
				self.jpt_pull.SetBinContent(j, pull)
		self.jpt_pull.Draw("")
		pad2.SetGridy()
		self.zero.Draw("same hist")
		
		c1.SaveAs("./ptslices/msd_total_datafine.png")
		
		
		ofile.WriteObject(self.Data_p7, "Data_pass_jet_pt_soft_coarse")
		ofile.WriteObject(self.Data_p9, "Data_pass_jet_pt_rho")
		ofile.WriteObject(self.Data_f7, "Data_fail_jet_pt_soft_coarse")
		ofile.WriteObject(self.Data_f9, "Data_fail_jet_pt_rho")
		ofile.WriteObject(self.back_est_msd, "back_est_msd")
		ofile.WriteObject(self.back_est_rho, "back_est_rho")
#		ofile.WriteObject(self.back_est_rho2, "back_est_rho2")
		ofile.WriteObject(self.Data_rpt, "rpt_TF")
		ofile.WriteObject(self.Data_mpt, "mpt_TF")
		
		
		
		ofile.Write()
