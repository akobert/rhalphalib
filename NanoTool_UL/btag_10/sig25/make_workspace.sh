cd output/testModel/

chmod +x build.sh

. build.sh

#text2workspace.py model_combined.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel
text2workspace.py model_combined.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO 'map=ptbin.*/Sig25:r[0,10]'
