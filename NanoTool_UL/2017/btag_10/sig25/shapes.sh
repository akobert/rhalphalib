#combine -M FitDiagnostics -m 125 output/testModel/model_combined.root --expectSignal 1 -t -1 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 -v 9
#combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 1
combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 1 --setParameters tf_dataResidual_pt_par0_rho_par0=1.66,tf_dataResidual_pt_par0_rho_par1=0.93,tf_dataResidual_pt_par0_rho_par2=0.87,tf_dataResidual_pt_par1_rho_par0=1.68,tf_dataResidual_pt_par1_rho_par1=0.91,tf_dataResidual_pt_par1_rho_par2=1.85,tf_dataResidual_pt_par2_rho_par0=0.55,tf_dataResidual_pt_par2_rho_par1=0.80,tf_dataResidual_pt_par2_rho_par2=0.90