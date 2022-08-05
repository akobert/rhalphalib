echo "Plotting Significance"
#combine -M Significance -m 125 --signif output/testModel/model_combined.root --cminDefaultMinimizerStrategy 0 -t -1 -v 9
#combine -M FitDiagnostics --signif output/testModel/model_combined.root --cminDefaultMinimizerStrategy 0 -t -1 -v 9 --redefineSignalPOI Sig10, Sig20, Sig25, Sig50, Sig75, Sig100, Sig125, Sig150
#combine -M FitDiagnostics --signif output/testModel/model_combined.root --cminDefaultMinimizerStrategy 0 -t -1 -v 9 --redefineSignalPOI rSig25 --setParameters rSig25=1
combine -M Significance --signif output/testModel/model_combined.root --cminDefaultMinimizerStrategy 0 -t -1 -v 0 --expectSignal 1
