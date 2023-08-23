from __future__ import print_function, division
import sys, os
import csv, json
import numpy as np
from scipy.interpolate import interp1d
import scipy.stats
import pickle
import ROOT
import pandas as pd

import rhalphalib as rl
rl.util.install_roofit_helpers()
rl.ParametericSample.PreferRooParametricHist = False

#def get_template(sName, passed, ptbin, cat, obs, syst, muon=False):
#    """
#    Read msd template from root file
#    """

#    f = ROOT.TFile.Open('signalregion.root')
#    if muon:
#        f = ROOT.TFile.Open('muonCR.root')

#    name = cat+'fail_'
#    if passed:
#        name = cat+'pass_'
#    if cat == 'ggf_':
#        name += 'pt'+str(ptbin)+'_'
#    if cat == 'vbf_':
#        name += 'mjj'+str(ptbin)+'_'

#    name += sName+'_'+syst

#    h = f.Get(name)
#    sumw = []
#    sumw2 = []

#    for i in range(1,h.GetNbinsX()+1):
#        sumw += [h.GetBinContent(i)]
#        sumw2 += [h.GetBinError(i)*h.GetBinError(i)]

#    return (np.array(sumw), obs.binning, obs.name, np.array(sumw2))

def get_template(sName, passed, ptbin, cat, obs, syst, muon=False):
    """
    Read msd template from root file
    """
    f = ROOT.TFile.Open('FitHist.root')

    name = 'fail'
    if passed:
        name = 'pass'

    name = sName+'_'+name+'_'+"jet_pt_soft_wide4"

    h = f.Get(name)
#    print("Template: "+name)
    sumw = []
    sumw2 = []
    for i in range(1, h.GetNbinsY()+1):
    #    if h.GetBinContent(ptbin, i) < 0:
    #        sumw += [0]
    #        sumw2 += [0]
    #    else:
	sumw += [h.GetBinContent(ptbin, i)]
        sumw2 += [h.GetBinError(ptbin, i)*h.GetBinError(ptbin, i)]

    integral = np.array(sumw).sum()
    print("For template "+name+" integral is "+str(integral))

    return (np.array(sumw), obs.binning, obs.name, np.array(sumw2))

def plot_mctf(tf_MCtempl, msdbins, name):
    """
    Plot the MC pass / fail TF as function of (pt,rho) and (pt,msd)
    """
    import matplotlib.pyplot as plt

    # arrays for plotting pt vs msd                    
    pts = np.linspace(450,1200,15)
    ptpts, msdpts = np.meshgrid(pts[:-1] + 0.5 * np.diff(pts), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
    ptpts_scaled = (ptpts - 450.) / (1200. - 450.)
    rhopts = 2*np.log(msdpts/ptpts)

    rhopts_scaled = (rhopts - (-6)) / ((-2.1) - (-6))
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

    fig, ax = plt.subplots()
    h = ax.hist2d(x=df["msd"],y=df["pt"],weights=df["MCTF"], bins=(msdbins,pts))
    plt.xlabel("$m_{sd}$ [GeV]")
    plt.ylabel("$p_{T}$ [GeV]")
    cb = fig.colorbar(h[3],ax=ax)
    cb.set_label("Ratio")
    fig.savefig("plots/MCTF_msdpt_"+name+".png",bbox="tight")
    fig.savefig("plots/MCTF_msdpt_"+name+".pdf",bbox="tight")
    plt.clf()

    # arrays for plotting pt vs rho                                          
    rhos = np.linspace(-6,-2.1,23)
    ptpts, rhopts = np.meshgrid(pts[:-1] + 0.5*np.diff(pts), rhos[:-1] + 0.5 * np.diff(rhos), indexing='ij')
    ptpts_scaled = (ptpts - 450.) / (1200. - 450.)
    rhopts_scaled = (rhopts - (-6)) / ((-2.1) - (-6))
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

    fig, ax = plt.subplots()
    h = ax.hist2d(x=df["rho"],y=df["pt"],weights=df["MCTF"],bins=(rhos,pts))
    plt.xlabel("rho")
    plt.ylabel("$p_{T}$ [GeV]")
    cb = fig.colorbar(h[3],ax=ax)
    cb.set_label("Ratio")
    fig.savefig("plots/MCTF_rhopt_"+name+".png",bbox="tight")
    fig.savefig("plots/MCTF_rhopt_"+name+".pdf",bbox="tight")

    return

def rhalphabet(tmpdir,
               throwPoisson = True,
               fast=0):
    """ 
    Create the data cards!
    """
    tqqnormSF = rl.NuisanceParameter('tqqnormSF_{}'.format(year), 'lnN',  1., 0, 10)
    WGnormSF = rl.NuisanceParameter('WGnormSF_{}'.format(year), 'lnN',  1., 0, 10)
    ZGnormSF = rl.NuisanceParameter('ZGnormSF_{}'.format(year), 'lnN',  1., 0, 10)

    # define bins    
#    ptbins = {}
#    ptbins['ggf'] = np.array([450, 500, 550, 600, 675, 800, 1200])
#    ptbins['vbf'] = np.array([450,1200])

#    mjjbins = {}
#    mjjbins['ggf'] = np.array([0,4000])
#    mjjbins['vbf'] = np.array([1000,2000,4000])

#    npt = {}
#    npt['ggf'] = len(ptbins['ggf']) - 1
#    npt['vbf'] = len(ptbins['vbf']) - 1

#    nmjj = {}
#    nmjj['ggf'] = len(mjjbins['ggf']) - 1
#    nmjj['vbf'] = len(mjjbins['vbf']) - 1

#    msdbins = np.linspace(40, 201, 24)
#    msd = rl.Observable('msd', msdbins)

#    validbins = {}

#    cats = ['vbf']
#    ncat = len(cats)

    ptbins = {}

    ptbins['sig25'] = np.array([120,130,145,160,180,200,250,300,400,500])
    npt = {}
    npt['sig25'] = len(ptbins['sig25']) - 1
    msdbins = np.linspace(0, 200, 41)

    msd = rl.Observable('msd', msdbins)

    validbins = {}

    cats = ['sig25']
    ncat = len(cats)

    # Build GJ MC pass+fail model and fit to polynomial
    tf_params = {}
    for cat in cats:
	print("Category: "+cat)

        fitfailed_GJ = 0

        # here we derive these all at once with 2D array                            
        ptpts, msdpts = np.meshgrid(ptbins[cat][:-1] + 0.5 * np.diff(ptbins[cat]), msdbins[:-1] + 0.5 * np.diff(msdbins), indexing='ij')
        rhopts = 2*np.log(msdpts/ptpts)
        print(ptpts)
        print(msdpts)
        print(rhopts)
	ptscaled = (ptpts - 120.0) / (500.0 - 120.0)
        rhoscaled = (rhopts - (-7.0)) / ((-2.0) - (-7.0))
        validbins[cat] = (rhoscaled >= 0) & (rhoscaled <= 1)
        rhoscaled[~validbins[cat]] = 1  # we will mask these out later   

        while fitfailed_GJ < 5:
        
            GJmodel = rl.Model('GJmodel_'+cat)
            GJpass, GJfail = 0., 0.
                	

            for ptbin in range(npt[cat]):
		
		failCh = rl.Channel('ptbin%d%s%s%s' % (ptbin, cat, 'fail',year))
                passCh = rl.Channel('ptbin%d%s%s%s' % (ptbin, cat, 'pass',year))
                GJmodel.addChannel(failCh)
                GJmodel.addChannel(passCh)

                # GJ templates from file                           
                failTempl = get_template('GJ', 0, ptbin+2, cat+'_', obs=msd, syst='nominal')
                passTempl = get_template('GJ', 1, ptbin+2, cat+'_', obs=msd, syst='nominal')

                failCh.setObservation(failTempl, read_sumw2=True)
                passCh.setObservation(passTempl, read_sumw2=True)

                GJfail += sum([val for val in failCh.getObservation()[0]])
		print("GJfail: "+str(GJfail))
                GJpass += sum([val for val in passCh.getObservation()[0]])
		print("GJpass: "+str(GJpass))

            GJeff = GJpass / GJfail
            print('Inclusive P/F from Monte Carlo = ' + str(GJeff))

            # initial values                                                                 
            print('Initial fit values read from file initial_vals*')
            with open('initial_vals_'+cat+'_mc.json') as f:
                initial_vals = np.array(json.load(f)['initial_vals'])
            print(initial_vals)

#            tf_MCtempl = rl.BasisPoly("tf_MCtempl_"+cat+year,
#                                      (initial_vals.shape[0]-1,initial_vals.shape[1]-1),
#                                      ['pt', 'rho'],
#                                      basis='Bernstein',
#                                      init_params=initial_vals,
#                                      limits=(-100, 100), coefficient_transform=None)

    	    tf_MCtempl = rl.BernsteinPoly("tf_MCtempl_"+cat+year, (initial_vals.shape[0]-1,initial_vals.shape[1]-1), ['pt', 'rho'], init_params=initial_vals, limits=(-100, 100))


            tf_MCtempl_params = GJeff * tf_MCtempl(ptscaled, rhoscaled)

            for ptbin in range(npt[cat]):

                failCh = GJmodel['ptbin%d%sfail%s' % (ptbin, cat, year)]
                passCh = GJmodel['ptbin%d%spass%s' % (ptbin, cat, year)]
                failObs = failCh.getObservation()
                passObs = passCh.getObservation()
                
                GJparams = np.array([rl.IndependentParameter('GJparam_ptbin%d%s%s_%d' % (ptbin, cat, year, i), 0) for i in range(msd.nbins)])
                sigmascale = 10.
                scaledparams = failObs * (1 + sigmascale/np.maximum(1., np.sqrt(failObs)))**GJparams
                
                fail_GJ = rl.ParametericSample('ptbin%d%sfail%s_GJ' % (ptbin, cat, year), rl.Sample.BACKGROUND, msd, scaledparams[0])
                failCh.addSample(fail_GJ)
                pass_GJ = rl.TransferFactorSample('ptbin%d%spass%s_GJ' % (ptbin, cat, year), rl.Sample.BACKGROUND, tf_MCtempl_params[ptbin, :], fail_GJ)
                passCh.addSample(pass_GJ)
                
                failCh.mask = validbins[cat][ptbin]
                passCh.mask = validbins[cat][ptbin]

            GJfit_ws = ROOT.RooWorkspace('w')

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
            GJfit_ws.writeToFile(os.path.join(str(tmpdir), 'testModel_GJfit_'+cat+'_'+year+'.root'))

            # Set parameters to fitted values  
            allparams = dict(zip(GJfit.nameArray(), GJfit.valueArray()))
            pvalues = []
            for i, p in enumerate(tf_MCtempl.parameters.reshape(-1)):
                p.value = allparams[p.name]
                pvalues += [p.value]
            
            if GJfit.status() != 0:
                print('Could not fit GJ')
                fitfailed_GJ += 1

            new_values = np.array(pvalues).reshape(tf_MCtempl.parameters.shape)
            with open("initial_vals_"+cat+"_mc.json", "w") as outfile:
                json.dump({"initial_vals":new_values.tolist()},outfile)

            else:
                break

        if fitfailed_GJ >=5:
            raise RuntimeError('Could not fit GJ after 5 tries')

        print("Fitted GJ for category " + cat)

        # Plot the MC P/F transfer factor                                                   
#        plot_mctf(tf_MCtempl,msdbins, cat)                           

        param_names = [p.name for p in tf_MCtempl.parameters.reshape(-1)]
        decoVector = rl.DecorrelatedNuisanceVector.fromRooFitResult(tf_MCtempl.name + '_deco', GJfit, param_names)
        tf_MCtempl.parameters = decoVector.correlated_params.reshape(tf_MCtempl.parameters.shape)
        tf_MCtempl_params_final = tf_MCtempl(ptscaled, rhoscaled)

#        tf_dataResidual = rl.BasisPoly("tf_dataResidual_"+year+cat,
#                                       (0,0),
#                                       ['pt', 'rho'],
#                                       basis='Bernstein',
#                                       init_params=np.array([[1]]),
#                                       limits=(-100,100),
#                                       coefficient_transform=None)

	tf_dataResidual = rl.BernsteinPoly("tf_dataResidual_"+cat+year, (0,0), ['pt', 'rho'], init_params=np.array([[1]]), limits=(-100, 100))


        tf_dataResidual_params = tf_dataResidual(ptscaled, rhoscaled)
#        with open('initial_vals_data_'+cat+'.json') as f:
#            initial_vals_data = np.array(json.load(f)['initial_vals'])
#        print("TFres order " + str(initial_vals_data.shape[0]-1)+ " in pT, " + str(initial_vals_data.shape[1]-1) + " in rho")
#        tf_dataResidual = rl.BasisPoly("tf_dataResidual_"+year+cat,
#                                       (initial_vals_data.shape[0]-1,initial_vals_data.shape[1]-1), 
#                                       ['pt', 'rho'], 
#                                       basis='Bernstein',
#                                       init_params=initial_vals_data,
#                                       limits=(-100,100), 
#                                       coefficient_transform=None)
        tf_params[cat] = GJeff * tf_MCtempl_params_final * tf_dataResidual_params

    # build actual fit model now
    model = rl.Model('testModel_'+year)

    # exclude GJ from MC samps
#    samps = ['ggF']
#    sigs = ['ggF']
    samps = ['TTBar', 'Sig25', 'WGamma', 'ZGamma']
    sigs = ['Sig25']

    for cat in cats:
        for ptbin in range(npt[cat]):
            for region in ['pass', 'fail']:


                # drop bins outside rho validity                                                
                mask = validbins[cat][ptbin]

                ch = rl.Channel('ptbin%d%s%s%s' % (ptbin, cat, region, year))
                model.addChannel(ch)

                isPass = region == 'pass'
                templates = {}
            
                for sName in samps:

                    templates[sName] = get_template(sName, isPass, ptbin+2, cat+'_', obs=msd, syst='nominal')
                    nominal = templates[sName][0]

                    # expectations
                    templ = templates[sName]
                        
                    if sName in sigs:
                        stype = rl.Sample.SIGNAL
                    else:
                        stype = rl.Sample.BACKGROUND
                    
                    sample = rl.TemplateSample(ch.name + '_' + sName, stype, templ)
                
                    ch.addSample(sample)

                # Observed data = GJ MC
                data_obs = get_template('GJ', isPass, ptbin+2, cat+'_', obs=msd, syst='nominal')

                ch.setObservation(data_obs, read_sumw2=True)

                # drop bins outside rho validity
                mask = validbins[cat][ptbin]

    for cat in cats:
        for ptbin in range(npt[cat]):

            failCh = model['ptbin%d%sfail%s' % (ptbin, cat, year)]
            passCh = model['ptbin%d%spass%s' % (ptbin, cat, year)]

            GJparams = np.array([rl.IndependentParameter('GJparam_ptbin%d%s%s_%d' % (ptbin, cat, year, i), 0) for i in range(msd.nbins)])
            initial_GJ = failCh.getObservation()[0].astype(float)  # was integer, and numpy complained about subtracting float from it                                
            if np.any(initial_GJ < 0.):
                raise ValueError('initial_GJ negative for some bins..', initial_GJ)

            sigmascale = 10  # to scale the deviation from initial                                                                                                     
            scaledparams = initial_GJ * (1 + sigmascale/np.maximum(1., np.sqrt(initial_GJ)))**GJparams
            fail_GJ = rl.ParametericSample('ptbin%d%sfail%s_GJ' % (ptbin, cat, year), rl.Sample.BACKGROUND, msd, scaledparams)
            failCh.addSample(fail_GJ)
            pass_GJ = rl.TransferFactorSample('ptbin%d%spass%s_GJ' % (ptbin, cat, year), rl.Sample.BACKGROUND, tf_params[cat][ptbin, :], fail_GJ)
            passCh.addSample(pass_GJ)
            

	    WGpass = passCh['WGamma']
            WGfail = failCh['WGamma']
            WGPF = WGpass.getExpectation(nominal=True).sum() / WGfail.getExpectation(nominal=True).sum()
            WGpass.setParamEffect(WGnormSF, 1.1)
            WGfail.setParamEffect(WGnormSF, 1.1*WGPF)

            ZGpass = passCh['ZGamma']
            ZGfail = failCh['ZGamma']
            ZGPF = ZGpass.getExpectation(nominal=True).sum() / ZGfail.getExpectation(nominal=True).sum()
            ZGpass.setParamEffect(ZGnormSF, 1.1)
            ZGfail.setParamEffect(ZGnormSF, 1.1*ZGPF)

            tqqpass = passCh['TTBar']
            tqqfail = failCh['TTBar']
            tqqPF = tqqpass.getExpectation(nominal=True).sum() / tqqfail.getExpectation(nominal=True).sum()
            tqqpass.setParamEffect(tqqnormSF, 1.1)
            tqqfail.setParamEffect(tqqnormSF, 1.1*tqqPF)

    with open(os.path.join(str(tmpdir), 'testModel_'+year+'.pkl'), 'wb') as fout:
        pickle.dump(model, fout)

    model.renderCombine(os.path.join(str(tmpdir), 'testModel_'+year))

if __name__ == '__main__':

    year = "2016"
    thisdir = os.getcwd()
    if "2016APV" in thisdir:
        year = "2016APV"
    elif "2017" in thisdir: 
        year = "2017"
    elif "2018" in thisdir:
        year = "2018"

    print("Running for "+year)

    if not os.path.exists('output'):
        os.mkdir('output')

    rhalphabet('output',year)

