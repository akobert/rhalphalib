#Copied from https://github.com/osherson/B2GAnalysis_2020/blob/master/analysis/CombineStep1.py
#And modified for my analysis
import ROOT
from ROOT import *
import numpy
import math
import sys
import array
import os
#import TEMPPAYLOAD
#from TEMPPAYLOAD import *

def GoodPlotFormat(H, *args): # Handy little script for color/line/fill/point/etc...
	try: H.SetStats(0)
	except: print " ------------ [  No stats box found!  ]"
	if args[0] == 'thickline':
		H.SetLineColor(args[1])
		H.SetLineWidth(2)
	if args[0] == 'thinline':
		H.SetLineColor(args[1])
		H.SetLineWidth(1)
		H.SetLineStyle(args[2])
	if args[0] == 'fill':
		H.SetLineColor(args[1])
		H.SetFillColor(args[1])
		H.SetFillStyle(args[2])
	if args[0] == 'markers':
		H.SetLineColor(args[1])
		H.SetMarkerColor(args[1])
		H.SetMarkerStyle(args[2])
	H.GetXaxis().SetTitleSize(0.04)

	if args[0] == 'dashed':
		H.SetLineColor(args[1])
		H.SetLineWidth(1)
		H.SetLineStyle(7)

def convertAsymGraph(TG, template, name):
	Hist = template.Clone(name)
	for i in range(1,Hist.GetNbinsX()+1):
		Hist.SetBinContent(i,0.)

#	print("Number of points: "+str(TG.GetN()))

	for i in range(TG.GetN()):
	#	Hist.SetBinContent(i+1,TG.GetY()[i]*(TG.GetErrorXlow(i)+TG.GetErrorXhigh(i)))
		Hist.SetBinContent(i+1,TG.GetY()[i])
#		print("Y= "+str(TG.GetY()[i]))
#		print("error xlow + error xhigh = "+str(TG.GetErrorXlow(i)+TG.GetErrorXhigh(i)))
		Hist.SetBinError(i+1, TG.GetErrorY(i))
	return Hist

def convertBinNHist(H, template, name):
	Hist = template.Clone(name)
	for i in range(1,Hist.GetNbinsX()+1):
		Hist.SetBinContent(i,H.GetBinContent(i))
		if H.GetBinContent(i) > 0 and (name == "dataprefitnewprefit" or name == "datafit_bnewfit_b" or name == "datafit_snewfit_s"):
	                Hist.SetBinError(i,math.sqrt(H.GetBinContent(i)))
		else:
			Hist.SetBinError(i,H.GetBinError(i))
	return Hist

def Reroll(H, VARS, ZOOM):
	X = TH1F("x_"+H.GetName(), ";"+VARS[2], len(VARS[1])-1, numpy.array(VARS[1]))
	Y = TH1F("y_"+H.GetName(), ";"+VARS[5], len(VARS[4])-1, numpy.array(VARS[4]))
		
	XY = TH2F("xy_"+H.GetName(), ";"+VARS[2]+";"+VARS[5], len(VARS[1])-1, numpy.array(VARS[1]), len(VARS[4])-1, numpy.array(VARS[4]))
	XYe = TH2F("xye_"+H.GetName(), ";"+VARS[2]+";"+VARS[5], len(VARS[1])-1, numpy.array(VARS[1]), len(VARS[4])-1, numpy.array(VARS[4]))

	X.SetStats(0)
	Y.SetStats(0)
	XY.SetStats(0)

	nxb = X.GetNbinsX()
	nyb = Y.GetNbinsX()

	for i in range(0,(nxb)):
		for j in range(0,(nyb)):
			k = XY.GetBin(i+1,j+1)
			index = H.FindBin(1 + j + i*nyb)
			XY.SetBinContent(k, H.GetBinContent(index))
			XY.SetBinError(k, (H.GetBinError(index)))
			XYe.SetBinContent(k, (H.GetBinError(index)))
	zoom_xl = XY.GetYaxis().FindBin(ZOOM[1][0])
	zoom_xh = XY.GetYaxis().FindBin(ZOOM[1][1])
	zoom_yl = XY.GetXaxis().FindBin(ZOOM[0][0])
	zoom_yh = XY.GetXaxis().FindBin(ZOOM[0][1])
	X = XY.ProjectionX("px_"+H.GetName(),1,nxb,"e")
	Y = XY.ProjectionY("py_"+H.GetName(),1,nyb,"e")
	zX = XY.ProjectionX("zpx_"+H.GetName(),zoom_xl,zoom_xh,"e")
	zY = XY.ProjectionY("zpy_"+H.GetName(),zoom_yl,zoom_yh,"e")
	return [X,Y,XY,XYe,zX,zY]

def MakeNBinsFromMinToMax(N,Min,Max): # helper for making large bin arrays makes N bins between Min and Max (same as you're feed to a TH1F)
	BINS = []
	for i in range(N+1):
		BINS.append(Min+(i*(Max-Min)/N))
	return BINS

def DBBW(H):
	for i in range(1,H.GetNbinsX()+1):
		C = H.GetBinContent(i)
		E = H.GetBinError(i)
		W = H.GetBinWidth(i)
		H.SetBinContent(i, C/W)
		H.SetBinError(i, E/W)	
	return H

def FindAndSetMax(*args):
	if len(args) == 1: args = args[0]
	maximum = 0.0
	for i in args:
		i.SetStats(0)
		t = i.GetMaximum()
		if t > maximum:
			maximum = t
	for j in args:
		j.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
		j.SetLineWidth(2)
	return maximum*1.35

def AddCMSLumi(pad, fb, extra):
	cmsText     = "CMS " + extra
	cmsTextFont   = 61  
	lumiTextSize     = 0.45
	lumiTextOffset   = 0.15
	cmsTextSize      = 0.5
	cmsTextOffset    = 0.15
	H = pad.GetWh()
	W = pad.GetWw()
	l = pad.GetLeftMargin()
	t = pad.GetTopMargin()
	r = pad.GetRightMargin()
	b = pad.GetBottomMargin()
	e = 0.025
	pad.cd()
	lumiText = str(fb)+" fb^{-1} (13 TeV)"
	latex = TLatex()
	latex.SetNDC()
	latex.SetTextAngle(0)
	latex.SetTextColor(kBlack)	
	extraTextSize = 0.76*cmsTextSize
	latex.SetTextFont(42)
	latex.SetTextAlign(31) 
	latex.SetTextSize(lumiTextSize*t)	
	latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
	pad.cd()
	latex.SetTextFont(cmsTextFont)
	latex.SetTextSize(cmsTextSize*t)
	latex.SetTextAlign(11)
	latex.DrawLatex(0.1265, 0.825, cmsText)
	pad.Update()


def pTbin(pad, Bin):
	cmsText     = "pT Bin: "+Bin+" GeV"
	cmsTextFont   = 61  
	cmsTextSize      = 0.5
	cmsTextOffset    = 0.15
	H = pad.GetWh()
	W = pad.GetWw()
	l = pad.GetLeftMargin()
	t = pad.GetTopMargin()
	r = pad.GetRightMargin()
	b = pad.GetBottomMargin()
	e = 0.025
	pad.cd()
	latex = TLatex()
	latex.SetNDC()
	latex.SetTextAngle(0)
	latex.SetTextColor(kBlack)	
	extraTextSize = 0.76*cmsTextSize
	pad.cd()
	latex.SetTextFont(cmsTextFont)
	latex.SetTextSize(cmsTextSize*t)
	latex.SetTextAlign(11)
	latex.DrawLatex(0.6, 0.525, cmsText)
	pad.Update()

def drawDiagnostic(name, ifile1):
	gROOT.SetBatch(True)
	Sigs = [["/home/akobert/CMSSW_11_1_0_pre7/src/RData/NanoTool_UL/M25_UL_nano_merged.root"], "5.467*7639.0/567896.0", "", "sig25_nano", "25 GeV Signal", "7639.0"]
	sig_name = "sig25_nano"
	ptBins = [120,130,145,160,180,200,250,300,400,500]
	mBins = MakeNBinsFromMinToMax(40,0,200)
	VAR = ["jpt", ptBins, "Jet pT (GeV)", "sdm", mBins, "Softdrop Mass (GeV)"]

	Blind = True
	LUMI = 5.467 #Temporary luminosity with 10% of 2018 data
	cmsextra = "Preliminary"

	pull_count = TH1F("pull_count", "Passing Pull Count", 100, -5, 5)
	pull_count_total = TH1F("pull_count_total", "Passing Pull Count Total", 100, -5, 5)

	ofile = ROOT.TFile("./fit_b_pull_count.root", "RECREATE")

	for pf in ["pass", "fail"]:
		for a in range(0, 9):
			print("ptbin #"+str(a))
			NAME = "ptbin"+str(a)+pf
			refF = ROOT.TFile("FitHist.root")
			refH = refF.Get("Data_"+pf+"_soft")
			CbnF = ROOT.TFile("fitDiagnosticsTest.root")
#			for P in ["prefit", "fit_b", "fit_s"]: 
#			for P in ["fit_b", "fit_s"]:
			for P in ["prefit", "fit_b"]:
					cDATA = CbnF.Get("shapes_"+P+"/"+NAME+"/data")
					cNRES = CbnF.Get("shapes_"+P+"/"+NAME+"/Data")	#Non-Resonant Background
					cTT = CbnF.Get("shapes_"+P+"/"+NAME+"/TTBar")
				#	cTT = cTT.Clone()
					cTBKG = CbnF.Get("shapes_"+P+"/"+NAME+"/total_background")
					cSIG = CbnF.Get("shapes_"+P+"/"+NAME+"/total_signal")
                                        cWG = CbnF.Get("shapes_"+P+"/"+NAME+"/WGamma")
                                        cZG = CbnF.Get("shapes_"+P+"/"+NAME+"/ZGamma")

					#Testing
#					print(cDATA.GetN())
#					print(cTT.GetNbinsX())
#					print(cTBKG.GetNbinsX())
#					print(cSIG.GetNbinsX())

					cDATA = convertAsymGraph(cDATA, cTT, "data"+P)
					Hvec = []

					for i in [cDATA, cTT, cTBKG, cSIG, cWG, cZG, cNRES]:
						i.Scale(5.0)
						Hvec.append(convertBinNHist(i, refH, i.GetName()+"new"+P))


		#			cDATA.SetLineColor(kBlack)
		#			cTT.SetLineColor(kRed)
		#			c1 = ROOT.TCanvas()
		#			c1.cd()
					
		#			cDATA.Draw("hist")
		#			cTT.Draw("same hist")
		#			cTBKG.Draw("same hist")
		#			L1 = ROOT.TLegend(0.48,0.6,0.86,0.86)
		#			L1.SetFillColor(0)
		#			L1.SetLineColor(0)
		#			L1.AddEntry(cDATA, "data", "PE")
		#			L1.AddEntry(cTBKG, "total background", "L")
		#			L1.AddEntry(cTT, "t#bar{t} component", "L")
		#			if P != "fit_b":
		#				cSIG.SetLineColor(kGreen+1)
		#				cSIG.Draw("same hist")
		#				L1.AddEntry(cSIG, sig_name, "F")
		#			c1.SaveAs("./"+P+"_data_test.png")
		#			c1.Close()
					
#					Pull2D = Hvec[0][2].Clone("pull"+P)
					
#					Cd = ROOT.TCanvas()
#					Cd.cd()
#					Pull2D.Draw("colz")
#					Cd.Print("results/"+NAME+"/Data2D_"+P+".png")
					
#					Pull2D.Add(Hvec[2][2], -1.)
#					Pull2D.Divide(Hvec[0][3])
#					Hvec[2][3].Divide(Hvec[0][3])
#					Pull2D.GetZaxis().SetRangeUser(-3.,3.)
					
					
#					C2 = ROOT.TCanvas()
#					C2.cd()
#					Pull2D.Draw("colz")
#					C2.Print("results/"+NAME+"/Pull2D_"+P+".png")
					
#					C2e = ROOT.TCanvas()
#					C2e.cd()
#					Hvec[3][2].Draw("colz")
#					C2e.Print("results/"+NAME+"/Sig2D_"+P+".png")
					
					savename = P+"_sdm_"+str(ptBins[a])+"-"+str(ptBins[a+1])
					ptbin = str(ptBins[a])+"-"+str(ptBins[a+1])
					#data = DBBW(Hvec[0])
					#GoodPlotFormat(data, "markers", ROOT.kBlack, 20)
					#bkg = DBBW(Hvec[2])
					#GoodPlotFormat(bkg,"thickline", ROOT.kBlue, 1)
					#GoodPlotFormat(data,"thickline", ROOT.kBlue, 1)
					#ttbar = DBBW(Hvec[1])
					#GoodPlotFormat(ttbar,"thickline", ROOT.kRed, 1)
					#sig = DBBW(Hvec[3])
					#GoodPlotFormat(sig, "fill", ROOT.kGreen+1, 3003)
                                        #s75 = DBBW(Hvec[4])
                                        #GoodPlotFormat(s75,"thickline", ROOT.kViolet, 1)
                                        #s100 = DBBW(Hvec[5])
                                        #GoodPlotFormat(s100,"thickline", ROOT.kOrange, 1)
					data = Hvec[0]
					GoodPlotFormat(data, "markers", ROOT.kBlack, 20)
					bkg = Hvec[2]
					GoodPlotFormat(bkg,"thickline", ROOT.kBlue, 1)
					#GoodPlotFormat(data,"thickline", ROOT.kBlue, 1)
					ttbar = Hvec[1]
					GoodPlotFormat(ttbar,"thickline", ROOT.kRed, 1)
					sig = Hvec[3]
					GoodPlotFormat(sig, "fill", ROOT.kGreen+1, 3003)
                                        WG = Hvec[4]
                                        GoodPlotFormat(WG,"thickline", ROOT.kViolet, 1)
                                        ZG = Hvec[5]
                                        GoodPlotFormat(ZG,"thickline", ROOT.kOrange, 1)
					nonRes = Hvec[6]
                                        GoodPlotFormat(nonRes,"dashed", ROOT.kCyan, 1)

					cheapline = data.Clone("cheapline")
					cheapline.Add(data,-1.)
					cheapline.GetYaxis().SetTitle("#frac{data - bkg}{#sigma_{data}}")
					cheapline.GetYaxis().SetTitleSize(0.175);
					cheapline.GetYaxis().SetNdivisions(6);
					cheapline.GetYaxis().SetLabelSize(0.145);
					cheapline.GetYaxis().SetTitleOffset(0.225);
					cheapline.GetYaxis().CenterTitle(True)
					cheapline.GetYaxis().SetRangeUser(-5.,5.)
					GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
					bkg.GetYaxis().SetTitle("Events / 5 GeV")
					bkg.GetYaxis().SetTitleOffset(0.5);
					bkg.GetYaxis().SetTitleSize(0.075);
#                                        if P == "prefit":
 #                                               print("PreFit Test sqrt: "+str(math.sqrt(bkg.GetBinContent(3))))
  #                                              print("PreFit Test Error: "+str(bkg.GetBinError(3)))
   #                                     if P == "fit_s":
    #                                            print("fit_s Test sqrt: "+str(math.sqrt(bkg.GetBinContent(3))))
     #                                           print("fit_s Test Error: "+str(bkg.GetBinError(3)))
      #                                  if P == "fit_b":
       #                                         print("fit_b Test sqrt: "+str(math.sqrt(bkg.GetBinContent(3))))
        #                                        print("fit_b Test Error: "+str(bkg.GetBinError(3)))

					FindAndSetMax(data, bkg)
						
					E = []
					EP = []
					for i in range(1,data.GetNbinsX()+1):
						Err = bkg.GetBinError(i)
						
						blX = bkg.GetBinLowEdge(i)
						blY = bkg.GetBinContent(i) - Err
						trX = bkg.GetBinWidth(i) + blX
						trY = bkg.GetBinContent(i) + Err
						tBox = ROOT.TBox(blX,blY,trX,trY)
						if  data.GetBinError(i) > 0:
							ue = Err/data.GetBinError(i)
						else:
							ue = Err/2.7
						ue = min(5.0, ue)
						tPBox = ROOT.TBox(blX, -1*ue, trX, ue)
						tBox.SetFillColor(25)
						tBox.SetFillStyle(3144)
						tPBox.SetFillColor(25)
						tPBox.SetFillStyle(3144)
						tBox.SetLineColor(ROOT.kWhite)
						tPBox.SetLineColor(ROOT.kWhite)
						E.append(tBox)
						EP.append(tPBox)
										
					bkg.GetXaxis().SetLabelSize(0)
					
					pull = data.Clone("pull")
					pull.Add(bkg, -1.)
					GoodPlotFormat(pull, "markers", ROOT.kBlack, 20)
					for i in range(pull.GetNbinsX()):
						if not data.GetBinContent(i+1) == 0:
							pull.SetBinContent(i+1, pull.GetBinContent(i+1)/data.GetBinError(i+1))
							pull.SetBinError(i+1, 1)		
							#Fill Pull Counter
							if pf == "pass" and P == "fit_b":
								pull_count.Fill(pull.GetBinContent(i+1)/data.GetBinError(i+1))
								pull_count_total.Fill(pull.GetBinContent(i+1)/data.GetBinError(i+1))
						else:
							pull.SetBinContent(i+1, 0)
							pull.SetBinError(i+1, 0)
					
					L = ROOT.TLegend(0.48,0.6,0.86,0.86)
					L.SetFillColor(0)
					L.SetLineColor(0)
					if not Blind: L.AddEntry(data, "data", "PE")
					L.AddEntry(bkg, "total background", "L")
					L.AddEntry(ttbar, "t#bar{t} component", "L")
                                        L.AddEntry(WG, "W+Gamma", "L")
                                        L.AddEntry(ZG, "Z+Gamma", "L")
					L.AddEntry(nonRes, "Non-Resonant Background", "L")
					L.AddEntry(E[0], "background uncertainty", "F")
					if P != "fit_b":  L.AddEntry(sig, sig_name, "F")
					C = ROOT.TCanvas()
					C.cd()
					p12 = ROOT.TPad("pad1", "tall",0,0.165,1,1)
					p22 = ROOT.TPad("pad2", "short",0,0.0,1.0,0.23)
					p22.SetBottomMargin(0.35)
					p12.Draw()
					p22.Draw()
					p12.cd() # top
					ROOT.gPad.SetTicks(1,1)
					bkg.Draw("hist")
					ttbar.Draw("histsame")
                                        WG.Draw("histsame")
                                        ZG.Draw("histsame")
					nonRes.Draw("histsame")
					if P != "fit_b": sig.Draw("histsame")
					for e in E: e.Draw("same")
					data.Draw("esame")
					L.Draw("same")
					ROOT.TGaxis.SetMaxDigits(3)
					p12.RedrawAxis()
					AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
					pTbin(ROOT.gPad, ptbin)
					p22.cd() # bottom
					ROOT.gPad.SetTicks(1,1)
					cheapline.GetXaxis().SetTitleSize(0.1925);
					cheapline.GetXaxis().SetLabelSize(0.16);
					cheapline.GetXaxis().SetTitleOffset(0.84);
					cheapline.Draw("hist")
					for e in EP: e.Draw("same")

					l1 = TLine(0,2,200,2)
					l1.SetLineColor(kGray)
					l1.SetLineWidth(1)
					l1.SetLineStyle(7)
					l2 = TLine(0,-2,200,-2)
					l2.SetLineColor(kGray)
					l2.SetLineWidth(1)
					l2.SetLineStyle(7)
					pull.Draw("esame")
					l1.Draw("same")
					l2.Draw("same")
					p22.RedrawAxis()
#					C.Print("results/"+NAME+"/"+savename+"_"+pf+str(a)+"_v4.root")
					C.Print("results/"+NAME+"/"+savename+"_"+pf+str(a)+"_"+str(name)+".png")
					if pf == "pass" and P == "fit_b":
						pull_name = P+"_"+pf+"_pull_count_bin"+str(a)
						ofile.WriteObject(pull_count, pull_name)

	ofile.WriteObject(pull_count_total, "fit_b_pass_pull_count_total")
