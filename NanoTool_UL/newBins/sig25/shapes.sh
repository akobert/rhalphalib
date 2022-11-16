#combine -M FitDiagnostics -m 125 output/testModel/model_combined.root --expectSignal 1 -t -1 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 -v 9
combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 2 --robustFit=1 --plots -v 1
