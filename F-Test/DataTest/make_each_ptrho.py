import os
import numpy as np
import json

if __name__ == '__main__':

    year = "2016"
    thisdir = os.getcwd()
    if "2016APV" in thisdir:
        year = "2016APV"
    elif "2017" in thisdir:
        year = "2017"
    elif "2018" in thisdir:
        year = "2018"

    for pt in range(0,6):
        for rho in range(0,6):
            print("pt = "+str(pt)+", rho = "+str(rho))
            # Make the directory and go there
            thedir = "pt"+str(pt)+"rho"+str(rho)
            if not os.path.isdir(thedir):
                os.mkdir(thedir)
            os.chdir(thedir)

            linkdir="/home/akobert/CMSSW_10_2_13/src/F-Test/InputHist/"

            # Link what you need
            os.system("mkdir plots")
#            os.system("ln -s "+linkdir+year+"/signalregion.root .")
#            os.system("ln -s "+linkdir+year+"/muonCR.root .")
#            os.system("cp "+linkdir+year+"/initial_vals_ggf.json .")
#            os.system("cp "+linkdir+year+"/initial_vals_vbf*.json .")
#            os.system("ln -s "+linkdir+"../lumi.json .")
#            os.system("ln -s "+linkdir+"sf.json .")
#            os.system("ln -s ../../make_cards.py .")
            os.system("ln -s ../../make_workspace.sh .")

            os.system("ln -s "+linkdir+year+"/FitHist.root .")
            os.system("ln -s ../../make_cards.py .")

            # Create your json files of initial values
#            if not os.path.isfile("initial_vals_data_ggf.json"):

#                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
#                thedict = {}
#                thedict["initial_vals"] = initial_vals
                        
#                with open("initial_vals_data_ggf.json", "w") as outfile:
#                    json.dump(thedict,outfile)

            # Create your json files of initial values                                                                           
            if not os.path.isfile("initial_vals_mc_sig25.json"):
                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
                thedict = {}
                thedict["initial_vals"] = initial_vals

                with open("initial_vals_mc_sig25.json", "w") as outfile:
                    json.dump(thedict,outfile)
            if not os.path.isfile("initial_vals_data_sig25.json"):
                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
                thedict = {}
                thedict["initial_vals"] = initial_vals

                with open("initial_vals_data_sig25.json", "w") as outfile:
                    json.dump(thedict,outfile)

            # Create your json files of initial values                                                                                          
#            if not os.path.isfile("initial_vals_data_vbfhi.json"):
#                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
#                thedict = {}
#                thedict["initial_vals"] = initial_vals

#                with open("initial_vals_data_vbfhi.json", "w") as outfile:
#                    json.dump(thedict,outfile)

            # Make the workspace
            os.system("./make_workspace.sh > rhal.out")

            # Run the first fit
            combine_cmd = "combine -M MultiDimFit -m 125 -d output/testModel_"+year+"/model_combined.root --saveWorkspace \
            -P rSig25 --floatOtherPOIs=0 -n \"Snapshot\" \
            --robustFit=1 --cminDefaultMinimizerStrategy=0 \
            --setParameters rSig25=1"
            os.system(combine_cmd)

            # Run the goodness of fit
            combine_cmd = "combine -M GoodnessOfFit -m 125 -d higgsCombineSnapshot.MultiDimFit.mH125.root \
            -n \"Observed\" --snapshotName MultiDimFit --bypassFrequentistFit --algo \"saturated\" \
            --setParameters rSig25=1"
            os.system(combine_cmd)
	    
	    combine_cmd = "combine -M FitDiagnostics -m 125 output/testModel_"+year+"/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 0"
            os.system(combine_cmd)
                
            os.chdir("../")
