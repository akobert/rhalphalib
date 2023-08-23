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

            # You will have to change this
            linkdir="/home/akobert/CMSSW_10_2_13/src/F-Test/InputHist/"

            os.system("ln -s "+linkdir+year+"/FitHist.root .")
            os.system("ln -s ../../make_cards_qcd.py .")

            # Create your json files of initial values
            if not os.path.isfile("initial_vals_sig25_mc.json"):

                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
                thedict = {}
                thedict["initial_vals"] = initial_vals

                with open("initial_vals_sig25_mc.json", "w") as outfile:
                    json.dump(thedict,outfile)
            if not os.path.isfile("initial_vals_sig25_data.json"):

                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
                thedict = {}
                thedict["initial_vals"] = initial_vals

                with open("initial_vals_sig25_data.json", "w") as outfile:
                    json.dump(thedict,outfile)
#            if not os.path.isfile("initial_vals_data_sig25.json"):

#                initial_vals = (np.full((pt+1,rho+1),1)).tolist()
#                thedict = {}
#                thedict["initial_vals"] = initial_vals
                        
#                with open("initial_vals_data_sig25.json", "w") as outfile:
#                    json.dump(thedict,outfile)

            # Create the workspace
            os.system("python make_cards_qcd.py > rhal.out") 

            # Make the workspace
            os.chdir("output/testModel_"+year)
            os.system("chmod +rwx build.sh")
            os.system("./build.sh")
            os.chdir("../../")

            # Run the first fit
#            combine_cmd = "combineTool.py -M MultiDimFit -m 125 -d output/testModel_"+year+"/model_combined.root --saveWorkspace \
#            --setParameters r=0 --freezeParameters r -n \"Snapshot\" \
#            --robustFit=1 --cminDefaultMinimizerStrategy 0"
            combine_cmd = "combine -M MultiDimFit -m 125 -d output/testModel_"+year+"/model_combined.root --saveWorkspace \
            --setParameters r=0 --freezeParameters r -n \"Snapshot\" \
            --robustFit=1 --cminDefaultMinimizerStrategy 0"
            os.system(combine_cmd)

            # Run the goodness of fit
#            combine_cmd = "combineTool.py -M GoodnessOfFit -m 125 -d higgsCombineSnapshot.MultiDimFit.mH125.root \
#            --snapshotName MultiDimFit --bypassFrequentistFit \
#            --setParameters r=0 --freezeParameters r \
#            -n \"Observed\" --algo \"saturated\" --cminDefaultMinimizerStrategy 0"
            combine_cmd = "combine -M GoodnessOfFit -m 125 -d higgsCombineSnapshot.MultiDimFit.mH125.root \
            --snapshotName MultiDimFit --bypassFrequentistFit \
            --setParameters r=0 --freezeParameters r \
            -n \"Observed\" --algo \"saturated\" --cminDefaultMinimizerStrategy 0"
            os.system(combine_cmd)

	    combine_cmd = "combine -M FitDiagnostics -m 125 output/testModel_"+year+"/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 0"
            os.system(combine_cmd)

            os.chdir("../")
