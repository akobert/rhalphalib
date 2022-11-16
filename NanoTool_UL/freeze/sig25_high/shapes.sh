#combine -M FitDiagnostics -m 125 output/testModel/model_combined.root --expectSignal 1 -t -1 --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 -v 9
#combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 1
combine -M FitDiagnostics output/testModel/model_combined.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --robustFit=1 --plots -v 1 --setParameters tf_dataResidual_pt_par0_rho_par0=1.31,tf_dataResidual_pt_par0_rho_par1=0.75,tf_dataResidual_pt_par0_rho_par2=0.70,tf_dataResidual_pt_par1_rho_par0=1.23,tf_dataResidual_pt_par1_rho_par1=1.15,tf_dataResidual_pt_par1_rho_par2=1.12,tf_dataResidual_pt_par2_rho_par0=0.68,tf_dataResidual_pt_par2_rho_par1=0.79,tf_dataResidual_pt_par2_rho_par2=0.59,tf_dataResidual_pt_par0_rho_par3=0.74,tf_dataResidual_pt_par1_rho_par3=0.56,tf_dataResidual_pt_par2_rho_par3=1.81,tf_dataResidual_pt_par3_rho_par0=0.38,tf_dataResidual_pt_par3_rho_par1=1.79,tf_dataResidual_pt_par3_rho_par2=-0.15,tf_dataResidual_pt_par3_rho_par3=-0.12 --freezeParameters tf_dataResidual_pt_par0_rho_par0,tf_dataResidual_pt_par0_rho_par1,tf_dataResidual_pt_par0_rho_par2,tf_dataResidual_pt_par1_rho_par0,tf_dataResidual_pt_par1_rho_par1,tf_dataResidual_pt_par1_rho_par2,tf_dataResidual_pt_par2_rho_par0,tf_dataResidual_pt_par2_rho_par1,tf_dataResidual_pt_par2_rho_par2,tf_dataResidual_pt_par0_rho_par3,tf_dataResidual_pt_par1_rho_par3,tf_dataResidual_pt_par2_rho_par3,tf_dataResidual_pt_par3_rho_par0,tf_dataResidual_pt_par3_rho_par1,tf_dataResidual_pt_par3_rho_par2,tf_dataResidual_pt_par3_rho_par3