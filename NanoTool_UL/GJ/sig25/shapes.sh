#combine -M FitDiagnostics -m 125 output/testModel/model_combined.root --expectSignal 1 -t -1 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 -v 9
#combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 1
combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 1 --setParameters tf_dataResidual_pt_par0_rho_par0=2.12,tf_dataResidual_pt_par0_rho_par1=0.96,tf_dataResidual_pt_par0_rho_par2=1.21,tf_dataResidual_pt_par1_rho_par0=0.96,tf_dataResidual_pt_par1_rho_par1=1.22,tf_dataResidual_pt_par1_rho_par2=1.05,tf_dataResidual_pt_par2_rho_par0=0.93,tf_dataResidual_pt_par2_rho_par1=0.95,tf_dataResidual_pt_par2_rho_par2=0.95