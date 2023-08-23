from __future__ import print_function, division
import sys
import os
import csv
import rhalphalib as rl
import numpy as np
import scipy.stats
import pickle
import ROOT
from ROOT import *
rl.util.install_roofit_helpers()
rl.ParametericSample.PreferRooParametricHist = False
import pandas as pd
import json

class AffineMorphTemplate(object):
    def __init__(self, hist):
        '''                                                                                                   
        hist: a numpy-histogram-like tuple of (sumw, edges)                                                       
        '''
        from scipy.interpolate import interp1d

        self.sumw = hist[0]
        self.edges = hist[1]
        self.norm = self.sumw.sum()
        self.mean = (self.sumw*(self.edges[:-1] + self.edges[1:])/2).sum() / self.norm
        self.cdf = interp1d(x=self.edges,
                            y=np.r_[0, np.cumsum(self.sumw / self.norm)],
                            kind='linear',
                            assume_sorted=True,
                            bounds_error=False,
                            fill_value=(0, 1),
                           )

    def get(self, shift=0., scale=1.):
        '''                                                                                                             
        Return a shifted and scaled histogram                                                                                      
        i.e. new edges = edges * scale + shift                                                                                      
        '''
        scaled_edges = (self.edges - shift) / scale
        return np.diff(self.cdf(scaled_edges)) * self.norm, self.edges

def syst_variation(numerator,denominator):
    """
    Get systematic variation relative to nominal (denominator)
    """
    var = np.divide(numerator,denominator)
    var[np.where(numerator==0)] = 1
    var[np.where(denominator==0)] = 1
    return var

def get_template(sName, passed, ptbin, obs, syst, muon=False):
    """
    Read msd template from root file
    """
    f = ROOT.TFile.Open('FitHist.root')

    name = 'fail'
    if passed:
        name = 'pass'

    name = sName+'_'+name+'_'+"jet_pt_soft_wide8"

    h = f.Get(name)
#    print("Template: "+name)
    sumw = []
    sumw2 = []
    #for i in range(1, h.GetNbinsX()+1):
    #for i in range(1, 11):
    for i in range(1, 41):
        sumw += [h.GetBinContent(ptbin, i)]
        sumw2 += [h.GetBinError(ptbin, i)*h.GetBinError(ptbin, i)]

    integral = np.array(sumw).sum()
    print("For template "+name+" integral is "+str(integral))
    
    return (np.array(sumw), obs.binning, obs.name, np.array(sumw2))

def get_template2(sName, passed, ptbin, obs, syst, muon=False):
    """
    Read msd template from root file
    """
    f = ROOT.TFile.Open('FitHist.root')

    name = 'fail'
    if passed:
        name = 'pass'

    name = sName+'_'+name+'_'+"jet_pt_soft_wide8"

    h = f.Get(name)
#    print("Template: "+name)
    sumw = []
    sumw2 = []
    #for i in range(1, 41):
    for i in range(1, 41):
        sumw += [h.GetBinContent(ptbin, i)]
        sumw2 += [h.GetBinError(ptbin, i)*h.GetBinError(ptbin, i)]

    integral = np.array(sumw).sum()
    print("For template "+name+" integral is "+str(integral))
    
    return (np.array(sumw), obs.binning, obs.name, np.array(sumw2))

def passfailSF(isPass, sName, ptbin, obs, mask, SF=1, SF_unc=0.1, muon=False):
    """
    Return (SF, SF_unc) for a pass/fail scale factor.
    """
    if isPass:
        return SF, 1. + SF_unc / SF
    else:
        _pass = get_template(sName, 1, ptbin, obs=obs, syst='nominal', muon=muon)
        _pass_rate = np.sum(_pass[0] * mask)

        _fail = get_template(sName, 0, ptbin, obs=obs, syst='nominal', muon=muon)
        _fail_rate = np.sum(_fail[0] * mask)

        if _fail_rate > 0:
            _sf = 1 + (1 - SF) * _pass_rate / _fail_rate
            _sfunc = 1. - SF_unc * (_pass_rate / _fail_rate)
            return _sf, _sfunc
        else:
            return 1, 1

def plot_mctf(tf_MCtempl, msdbins):
    """
    Plot the MC pass / fail TF as function of (pt,rho) and (pt,msd)
    """
    import matplotlib.pyplot as plt
    
    ofile = ROOT.TFile("TF_Data.root", "RECREATE")
    ofile.cd()

    # arrays for plotting pt vs msd                    
    #pts = np.linspace(0,2000,41)
    pts = np.array([0,120, 170, 220, 300, 400, 700,900,1200,1500,2000])
    #ptpts, msdpts = np.meshgrid(pts[:-1] + 0.5 * np.diff(pts), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    ptpts, msdpts = np.meshgrid(pts[:-1] + 0.5 * np.diff(pts), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    ptpts_scaled = (ptpts) / (2000.)
    
    rhopts = 2*np.log(msdpts/ptpts)

    rhopts_scaled = (rhopts - (-7.0)) / ((-1.9) - (-7.0))
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
   
    ROOT.gInterpreter.Declare("Double_t widebins8[9] = {0, 120, 170, 220, 300, 400, 700, 1200, 2000};") 
    mpt_TF = TH2F("mpt_TF", "Mass vs. pT Transfer Factor", 8, widebins, 40, 0, 2000)
    for i in range(0, mpt.shape[0]):
        mpt_TF.Fill(mpt[i][0], mpt[i][1], mpt[i][2])
#	print(mpt[i][2])
    
    ofile.WriteObject(mpt_TF, "mpt_TF")

    fig, ax = plt.subplots()
    h = ax.hist2d(x=df["msd"],y=df["pt"],weights=df["MCTF"], bins=(msdbins,pts))
    plt.xlabel("$m_{sd}$ [GeV]")
    plt.ylabel("$p_{T}$ [GeV]")
    cb = fig.colorbar(h[3],ax=ax)
    cb.set_label("Ratio")
    fig.savefig("MCTF_msdpt_2018_sig25v2.png",bbox="tight")
    plt.clf()

    # arrays for plotting pt vs rho                                          
    rhos = np.linspace(-7.0,-1.9,41)
    #ptpts, rhopts = np.meshgrid(pts[:-1] + 0.5*np.diff(pts), rhos[:-1] + 0.5 * np.diff(rhos), indexing='ij')
    ptpts, rhopts = np.meshgrid(pts[:-1] + 0.5*np.diff(pts), rhos[:-1] + 0.5 * np.diff(rhos), indexing='ij')
    ptpts_scaled = (ptpts) / (2000)
    rhopts_scaled = (rhopts - (-7.0)) / ((-1.9) - (-7.0))
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

    rpt_TF = TH2F("rpt_TF", "Rho vs. pT Transfer Factor", 40, -9, 0, 40, 0, 2000)
    for i in range(0, rpt.shape[0]):
        rpt_TF.Fill(rpt[i][0], rpt[i][1], rpt[i][2])

    
    ofile.WriteObject(rpt_TF, "rpt_TF")
    
    
    
    fig, ax = plt.subplots()
    h = ax.hist2d(x=df["rho"],y=df["pt"],weights=df["MCTF"],bins=(rhos,pts))
    plt.xlabel("rho")
    plt.ylabel("$p_{T}$ [GeV]")
    cb = fig.colorbar(h[3],ax=ax)
    cb.set_label("Ratio")
    fig.savefig("MCTF_rhopt_2018_sig25v2.png",bbox="tight")

    return

def test_rhalphabet(tmpdir,
                    throwPoisson = True,
                    fast=0):
    """ 
    Create the data cards!
    """
#    with open('sf.json') as f:
#        SF = json.load(f)

    # TT params
#    tqqeffSF = rl.IndependentParameter('tqqeffSF_{}'.format(year), 1., 0, 10)
#    tqqnormSF = rl.IndependentParameter('tqqnormSF_{}'.format(year), 1., 0, 10)
#    WGeffSF = rl.IndependentParameter('WGeffSF_{}'.format(year), 1., 0, 10)
#    WGnormSF = rl.IndependentParameter('WGnormSF_{}'.format(year), 1., 0, 10)
#    ZGeffSF = rl.IndependentParameter('ZGeffSF_{}'.format(year), 1., 0, 10)
#    ZGnormSF = rl.IndependentParameter('ZGnormSF_{}'.format(year), 1., 0, 10)


#    tqqeffSF = rl.IndependentParameter('tqqeffSF_{}'.format(year), 1., 0, 10)
    tqqeffSF = rl.NuisanceParameter('tqqeffSF_{}'.format(year), 'lnN', 1., 0, 10)
#    tqqnormSF = rl.NuisanceParameter('tqqnormSF_{}'.format(year), 'lnN',  1., 0, 10)
#    WGeffSF = rl.IndependentParameter('WGeffSF_{}'.format(year), 1., 0, 10)
    WGeffSF = rl.NuisanceParameter('WGeffSF_{}'.format(year), 'lnN', 1., 0, 10)
#    WGnormSF = rl.NuisanceParameter('WGnormSF_{}'.format(year), 'lnN',  1., 0, 10)
#    ZGeffSF = rl.IndependentParameter('ZGeffSF_{}'.format(year), 1., 0, 10)
    ZGeffSF = rl.NuisanceParameter('ZGeffSF_{}'.format(year), 'lnN', 1., 0, 10)
#    ZGnormSF = rl.NuisanceParameter('ZGnormSF_{}'.format(year), 'lnN',  1., 0, 10)

    # define bins    
    ptbins = np.array([120, 170, 220, 300, 400, 700])
#    ptbins = np.linspace(100, 600, 11)
    npt = len(ptbins) - 1
#    msdbins = np.linspace(0, 100, 21)
#    msdbins = np.linspace(0, 50, 11)
    msdbins = np.linspace(0, 200, 41)
    msd = rl.Observable('msd', msdbins)

    # here we derive these all at once with 2D array
    ptpts, msdpts = np.meshgrid(ptbins[:-1] + 0.5 * np.diff(ptbins), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    #ptpts, msdpts = np.meshgrid(ptbins[:-1] + 0.5 * np.diff(ptbins), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    print(ptpts)
    print(msdpts)
    rhopts = 2*np.log(msdpts/ptpts)
    print(rhopts)
    ptscaled = (ptpts - 120.0) / (700.0 - 120.0)
    rhoscaled = (rhopts - (-7.0)) / ((-1.9) - (-7.0))
    validbins = (rhoscaled >= 0) & (rhoscaled <= 1)
    rhoscaled[~validbins] = 1  # we will mask these out later

    # Build MC pass+fail model and fit to polynomial
    GJmodel = rl.Model('GJmodel')
    GJpass, GJfail = 0., 0.
    pass_count, fail_count = 0., 0.
    for ptbin in range(npt):
        failCh = rl.Channel('ptbin%d%s' % (ptbin, 'fail'))
        passCh = rl.Channel('ptbin%d%s' % (ptbin, 'pass'))
        GJmodel.addChannel(failCh)
        GJmodel.addChannel(passCh)

        # GJ templates from file
        failTempl = get_template('GJ', 0, ptbin+2, obs=msd, syst='nominal') 
        passTempl = get_template('GJ', 1, ptbin+2, obs=msd, syst='nominal') 
        

        failCh.setObservation(failTempl, read_sumw2=True)
        passCh.setObservation(passTempl, read_sumw2=True)


        GJfail += sum([val for val in failCh.getObservation()[0]])
        fail_count += sum([val for val in failCh.getObservation()[0]])

	print(GJfail)
	print(fail_count)
        GJpass += sum([val for val in passCh.getObservation()[0]])
        pass_count += sum([val for val in passCh.getObservation()[0]])
	print(GJpass)
	print(pass_count)

    GJeff = GJpass / GJfail
    print('Inclusive P/F from Monte Carlo = ' + str(GJeff))

    # initial values
    print('Initial fit values read from file initial_vals.csv')
    initial_vals = np.genfromtxt('initial_vals.csv')
    initial_vals = initial_vals.reshape(4, 4)
    print(initial_vals)

    tf_MCtempl = rl.BernsteinPoly('tf_MCtempl', (3, 3), ['pt', 'rho'], init_params=initial_vals, limits=(-50, 50))
    tf_MCtempl_params = GJeff * tf_MCtempl(ptscaled, rhoscaled)
    for ptbin in range(npt):
        failCh = GJmodel['ptbin%dfail' % ptbin]
        passCh = GJmodel['ptbin%dpass' % ptbin]
        #failObs = failCh.getObservation().astype(float)
        #passObs = passCh.getObservation().astype(float)
        failObs = failCh.getObservation()
        passObs = passCh.getObservation()


	print(np.size(failObs))

	if np.any(failObs < 0):
	    for i in range(np.size(failObs[0])):
		if failObs[0][i] < 0:
		   failObs[0][i] = 0
		   failObs[1][i] = 0
	if np.any(passObs < 0):
	    for i in range(np.size(passObs[0])):
		if passObs[0][i] < 0:
		   passObs[0][i] = 0
		   passObs[1][i] = 0


        GJparams = np.array([rl.IndependentParameter('GJparam_ptbin%d_msdbin%d' % (ptbin, i), 0) for i in range(msd.nbins)])
        sigmascale = 10.
        scaledparams = failObs * (1 + sigmascale/np.maximum(1., np.sqrt(failObs)))**GJparams

        fail_GJ = rl.ParametericSample('ptbin%dfail_GJ' % ptbin, rl.Sample.BACKGROUND, msd, scaledparams[0])
        failCh.addSample(fail_GJ)
        pass_GJ = rl.TransferFactorSample('ptbin%dpass_GJ' % ptbin, rl.Sample.BACKGROUND, tf_MCtempl_params[ptbin, :], fail_GJ)
        passCh.addSample(pass_GJ)

        failCh.mask = validbins[ptbin]
        passCh.mask = validbins[ptbin]

    GJfit_ws = ROOT.RooWorkspace('GJfit_ws')

    simpdf, obs = GJmodel.renderRoofit(GJfit_ws)
    GJfit = simpdf.fitTo(obs,
                          ROOT.RooFit.Extended(True),
                          ROOT.RooFit.SumW2Error(True),
                          ROOT.RooFit.Strategy(2),
        		  ROOT.RooFit.Offset(True),
	                  ROOT.RooFit.Save(),
                          ROOT.RooFit.Minimizer('Minuit2', 'migrad'),
                          ROOT.RooFit.PrintLevel(1),
                          )
    GJfit_ws.add(GJfit)
    GJfit_ws.writeToFile(os.path.join(str(tmpdir), 'testModel_GJfit.root'))

	

    # Set parameters to fitted values  
    allparams = dict(zip(GJfit.nameArray(), GJfit.valueArray()))
    for i, p in enumerate(tf_MCtempl.parameters.reshape(-1)):
        p.value = allparams[p.name]
        print(p.name,p.value)

    if GJfit.status() != 0:
        raise RuntimeError('Could not fit GJ')
    
     #Plot the MC P/F transfer factor
    msdbins = np.linspace(0, 200, 41) 
#    plot_mctf(tf_MCtempl,msdbins)
   
    #New Stuff
    # Redefine bins
    ptbins = np.array([120, 170, 220, 300, 400, 700])
    npt = len(ptbins) - 1
    msdbins = np.linspace(0, 200, 41)
    msd = rl.Observable('msd', msdbins)

    # here we derive these all at once with 2D array
    #ptpts, msdpts = np.meshgrid(ptbins[:-1] + 0.5 * np.diff(ptbins), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    ptpts, msdpts = np.meshgrid(ptbins[:-1] + 0.5 * np.diff(ptbins), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    rhopts = 2*np.log(msdpts/ptpts)
    ptscaled = (ptpts - 120.0) / (700.0 - 120.0)
    rhoscaled = (rhopts - (-7.0)) / ((-1.9) - (-7.0))
    validbins = (rhoscaled >= 0) & (rhoscaled <= 1)
    rhoscaled[~validbins] = 1  # we will mask these out later

    param_names = [p.name for p in tf_MCtempl.parameters.reshape(-1)]
    decoVector = rl.DecorrelatedNuisanceVector.fromRooFitResult(tf_MCtempl.name + '_deco', GJfit, param_names)
    tf_MCtempl.parameters = decoVector.correlated_params.reshape(tf_MCtempl.parameters.shape)
    tf_MCtempl_params_final = tf_MCtempl(ptscaled, rhoscaled)
    tf_dataResidual = rl.BernsteinPoly('tf_dataResidual', (3, 3), ['pt', 'rho'], limits=(-50, 50))
    tf_dataResidual_params = tf_dataResidual(ptscaled, rhoscaled)
    #tf_params = Dataeff * tf_MCtempl_params_final * tf_dataResidual_params
    tf_params = GJeff * tf_MCtempl_params_final * tf_dataResidual_params

    # build actual fit model now
    model = rl.Model('testModel')

    # exclude GJ from MC samps
#    samps = ['ggF','VBF','WH','ZH','ttH','ttbar','singlet','Zjets','Wjets','VV']
#    sigs = ['ggF','VBF','WH','ZH','ttH']
    samps = ['TTBar','Sig25', 'WGamma', 'ZGamma']
    sigs = ['Sig25']
    for ptbin in range(npt):
        for region in ['pass', 'fail']:

            # drop bins outside rho validity                                                            
            mask = validbins[ptbin]

            ch = rl.Channel('ptbin%d%s' % (ptbin, region))
            model.addChannel(ch)

            isPass = region == 'pass'
            templates = {}

            for sName in samps:
		print("Sample "+region+" "+sName)
                templates[sName] = get_template2(sName, isPass, ptbin+2, obs=msd, syst='nominal')
                nominal = templates[sName][0]

                # expectations
                templ = templates[sName]
                stype = rl.Sample.SIGNAL if sName in sigs else rl.Sample.BACKGROUND
                sample = rl.TemplateSample(ch.name + '_' + sName, stype, templ)
	
		print(sName+" "+region+" Expectation: "+str(sample.getExpectation(nominal=True).sum()))

		
                ch.addSample(sample)

            data_obs = get_template2('Data', isPass, ptbin+2, obs=msd, syst='nominal')
            ch.setObservation(data_obs, read_sumw2=True)
    

            # drop bins outside rho validity
            mask = validbins[ptbin]

            # blind bins 11, 12, 13
 #           mask[11:14] = False
            ch.mask = mask
    test = model['ptbin0fail']
    print("Test: "+str(test['TTBar'].getExpectation(nominal=True).sum()))

    for ptbin in range(npt):
        failCh = model['ptbin%dfail' % ptbin]
        passCh = model['ptbin%dpass' % ptbin]
        Dataparams = np.array([rl.IndependentParameter('Dataparam_ptbin%d_msdbin%d' % (ptbin, i), 0) for i in range(msd.nbins)])
        initial_Data = failCh.getObservation()[0].astype(float)  # was integer, and numpy complained about subtracting float from it

        for sample in failCh:
	    if sample.sampletype == rl.Sample.BACKGROUND:#Subtract out backgrounds from fail
            	initial_Data -= sample.getExpectation(nominal=True)
		print("Subtract Sample: "+str(sample.name))


        if np.any(initial_Data < 0.):
#            raise ValueError('initial_Data negative for some bins..', initial_Data)
	    for i in range(np.size(initial_Data)):
		if initial_Data[i] < 0:
		   initial_Data[i] = 0
	    

        sigmascale = 10  # to scale the deviation from initial
        scaledparams = initial_Data * (1 + sigmascale/np.maximum(1., np.sqrt(initial_Data)))**Dataparams
        fail_Data = rl.ParametericSample('ptbin%dfail_Data' % ptbin, rl.Sample.BACKGROUND, msd, scaledparams)
        failCh.addSample(fail_Data)
        pass_Data = rl.TransferFactorSample('ptbin%dpass_Data' % ptbin, rl.Sample.BACKGROUND, tf_params[ptbin, :], fail_Data)
        passCh.addSample(pass_Data)

        WGpass = passCh['WGamma']
        WGfail = failCh['WGamma']
        WGPF = WGpass.getExpectation(nominal=True).sum() / WGfail.getExpectation(nominal=True).sum()
        WGpass.setParamEffect(WGeffSF, 1.1)
        WGfail.setParamEffect(WGeffSF, 1.1 * WGPF)

        ZGpass = passCh['ZGamma']
        ZGfail = failCh['ZGamma']
        ZGPF = ZGpass.getExpectation(nominal=True).sum() / ZGfail.getExpectation(nominal=True).sum()
        ZGpass.setParamEffect(ZGeffSF, 1.1)
        ZGfail.setParamEffect(ZGeffSF, (1.1) * ZGPF)

        tqqpass = passCh['TTBar']
        tqqfail = failCh['TTBar']
        tqqPF = tqqpass.getExpectation(nominal=True).sum() / tqqfail.getExpectation(nominal=True).sum()
#        tqqpass.setParamEffect(tqqeffSF, 1*tqqeffSF)
#        tqqfail.setParamEffect(tqqeffSF, (1-tqqeffSF) * tqqPF + 1)
        tqqpass.setParamEffect(tqqeffSF, 1.1)
        tqqfail.setParamEffect(tqqeffSF, 1.1 * tqqPF)
#    # Fill in muon CR
#    templates = {}
#    samps = ['ttbar','GJ','singlet','Zjets','Wjets','VV']
#    for region in ['pass', 'fail']:
#        ch = rl.Channel('muonCR%s' % (region, ))
#        model.addChannel(ch)

#        isPass = region == 'pass'

#        for sName in samps:
#            templates[sName] = get_template(sName, isPass, -1, obs=msd, syst='nominal', muon=True)

#            stype = rl.Sample.BACKGROUND
#            sample = rl.TemplateSample(ch.name + '_' + sName, stype, templates[sName])

#            ch.addSample(sample)

#        data_obs = get_template('muondata', isPass, -1, obs=msd, syst='nominal', muon=True)
#        ch.setObservation(data_obs, read_sumw2=True)
#    tqqpass = model['muonCRpass_ttbar']
#    tqqfail = model['muonCRfail_ttbar']
#    tqqPF = tqqpass.getExpectation(nominal=True).sum() / tqqfail.getExpectation(nominal=True).sum()
#    tqqpass.setParamEffect(tqqeffSF, 1*tqqeffSF)
#    tqqfail.setParamEffect(tqqeffSF, (1 - tqqeffSF) * tqqPF + 1)
#    tqqpass.setParamEffect(tqqnormSF, 1*tqqnormSF)
#    tqqfail.setParamEffect(tqqnormSF, 1*tqqnormSF)

    with open(os.path.join(str(tmpdir), 'testModel.pkl'), 'wb') as fout:
        pickle.dump(model, fout)

    model.renderCombine(os.path.join(str(tmpdir), 'testModel'))
    
 

if __name__ == '__main__':

    year = sys.argv[1]
    if not os.path.exists('output'):
        os.mkdir('output')

    test_rhalphabet('output',year)
    
    print("Rhalphalib Done")
