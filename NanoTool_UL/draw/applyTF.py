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

		PF = 0.10167698269829223

		#Output Files
	        ofile = ROOT.TFile(name + ".root", "RECREATE")
	        ofile.cd()


		#background files
		self.f = TFile.Open(bfile1, "READ")
		self.f.ls();


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
		final_vals = final_vals.reshape(6,6)

		tf_MCtempl = rl.BernsteinPoly('tf_MCtempl', (5, 5), ['pt', 'rho'], init_params=final_vals, limits=(-100, 100))
		
		msdbins = np.linspace(0, 200, 41)
		pts = np.array([120,130,145,160,180,200,250,300,400,500])
		ptpts, msdpts = np.meshgrid(pts[:-1] + 0.5 * np.diff(pts), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
		ptpts_scaled = (ptpts - 120.) / (500. - 120.)

		rhopts = 2*np.log(msdpts/ptpts)
		rhopts_scaled = (rhopts - (-7.)) / ((-2.0) - (-7.))
	
		validbins = (rhopts_scaled >= 0) & (rhopts_scaled <= 1)

    		ptpts = ptpts[validbins]
    		msdpts = msdpts[validbins]
    		ptpts_scaled = ptpts_scaled[validbins]
    		rhopts_scaled = rhopts_scaled[validbins]
	
		tf_MCtempl_vals = tf_MCtempl(ptpts_scaled, rhopts_scaled, nominal=True)

		combine_vals = np.genfromtxt('combine_out.csv')
		combine_vals = combine_vals.reshape(6,6)

		tf_MCtempl_params_final = tf_MCtempl(ptpts_scaled, rhopts_scaled, nominal=True)
		tf_dataResidual = rl.BernsteinPoly('tf_dataResidual', (5, 5), ['pt', 'rho'], init_params=combine_vals, limits=(-100, 100))
		tf_dataResidual_params = tf_dataResidual(ptpts_scaled, rhopts_scaled, nominal=True)
		tf_params = PF * tf_MCtempl_params_final * tf_dataResidual_params

		print(tf_params)

    		df = pd.DataFrame([])
    		df['msd'] = msdpts.reshape(-1)
    		df['pt'] = ptpts.reshape(-1)
    		#df['MCTF'] = tf_MCtempl_vals.reshape(-1)
    		#df['MCTF'] = tf_params.reshape(-1)
    		df['MCTF'] = tf_params


        	ROOT.gInterpreter.Declare("Double_t widebins4[16] = {0, 120, 130, 145, 160, 180, 200, 250, 300, 400, 500, 700, 900, 1200, 1500, 2000};")

		ROOT.gInterpreter.Declare("Double_t widebins[10] = {120, 130, 145, 160, 180, 200, 250, 300, 400, 500};")


    		mpt = df.to_numpy()
		mpt_TF_test = TH2F("mpt_TF_test", "pT vs. Mass Transfer Factor", 9, widebins, 40, 0, 200)
		#mpt_TF_test = TH2F("mpt_TF_test", "pT vs. Mass Transfer Factor", 15, widebins4, 40, 0, 200)

		mpt_TF_test.SetXTitle("Jet pT")
		mpt_TF_test.SetYTitle("Softdrop Mass")

		for i in range(0, mpt.shape[0]):
			print("Mass: "+str(mpt[i][0])+" pT: "+str(mpt[i][1])+" TF: "+str(mpt[i][2]))
        		mpt_TF_test.Fill(mpt[i][1], mpt[i][0], mpt[i][2])
#       		print(mpt[i][2])

		ofile.WriteObject(mpt_TF_test, "mpt_TF_test")

		rhos = np.linspace(-7.0,-2.0,41)
		pts = np.array([120,130,145,160,180,200,250,300,400,500])
    		ptpts, rhopts = np.meshgrid(pts[:-1] + 0.5*np.diff(pts), rhos[:-1] + 0.5 * np.diff(rhos), indexing='ij')
    		ptpts_scaled = (ptpts - 120.) / (500. - 120.)
   		rhopts_scaled = (rhopts - (-7.0)) / ((-2.0) - (-7.0))
    		validbins = (rhopts_scaled >= 0) & (rhopts_scaled <= 1)

    		ptpts = ptpts[validbins]
    		rhopts = rhopts[validbins]
    		ptpts_scaled = ptpts_scaled[validbins]
    		rhopts_scaled = rhopts_scaled[validbins]

    		tf_MCtempl_params_final = tf_MCtempl(ptpts_scaled, rhopts_scaled, nominal=True)
		tf_dataResidual = rl.BernsteinPoly('tf_dataResidual', (5, 5), ['pt', 'rho'], init_params=combine_vals, limits=(-100, 100))
		tf_dataResidual_params = tf_dataResidual(ptpts_scaled, rhopts_scaled, nominal=True)
		tf_params = PF * tf_MCtempl_params_final * tf_dataResidual_params

		print(tf_params)

    		df = pd.DataFrame([])
    		df['rho'] = rhopts.reshape(-1)
    		df['pt'] = ptpts.reshape(-1)
    		#df['MCTF'] = tf_MCtempl_vals.reshape(-1)
    		#df['MCTF'] = tf_params.reshape(-1)
    		df['MCTF'] = tf_params

    		rpt = df.to_numpy()

    		rpt_TF_test = TH2F("rpt_TF_test", "Rho vs. pT Transfer Factor", 40, -7, -2, 9, widebins)
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

	
#		self.back_est_msd = TH2F("back_est_msd", "MSD Background Estimate (P/F * TF * Fail)", 40, 0, 2000, 40, 0, 200)
#		self.back_est_msd.SetXTitle("Jet pT")
#		self.back_est_msd.SetYTitle("msd")
#		for i in range(1, self.back_est_msd.GetNbinsX()+1):
#			for j in range(1, self.back_est_msd.GetNbinsY()+1):
#				fail_mpt = self.Data_f7.GetBinContent(i,j)
#				TF = self.Data_mpt2.GetBinContent(i,j)
#				self.back_est_msd.SetBinContent(i, j, PF*TF*fail_mpt)
		




#		self.back_est_rho = TH2F("back_est_rho", "Rho Background Estimate (P/F * TF * Fail)", 40, 0, 2000, 40, -7, -2)
#		self.back_est_rho.SetXTitle("Jet pT")
#		self.back_est_rho.SetYTitle("rho")

#		for i in range(1, self.back_est_rho.GetNbinsX()+1):
#			for j in range(1, self.back_est_rho.GetNbinsY()+1):
#				fail_rpt = self.Data_f9.GetBinContent(i,j+4) #+4 because of different min
#				TF = self.Data_rpt2.GetBinContent(i,j)
#				self.back_est_rho.SetBinContent(i, j, PF*TF*fail_rpt)
		


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

		
		
#		ofile.WriteObject(self.back_est_msd, "back_est_msd")
#		ofile.WriteObject(self.back_est_rho, "back_est_rho")
#		ofile.WriteObject(self.back_est_rho2, "back_est_rho2")
		ofile.WriteObject(self.Data_rpt, "rpt_TF")
		ofile.WriteObject(self.Data_mpt, "mpt_TF")
		
		
		
		ofile.Write()
