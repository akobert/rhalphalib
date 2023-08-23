/************************************************
 *  * Jennet Dickinson 
 *   * Nov 19, 2020
 *    * Draw Roofit plots
 *     ************************************************/
#include <iostream>

using namespace RooFit;
using namespace RooStats;

//gROOT.SetBatch(True);

void draw_PFratio_MC(){

  // Get the year from the running directory   
  string thisdir = gSystem->pwd();

//  string year = "2016";

//  if(thisdir.find("2017") != std::string::npos){
//    year = "2017";
//  }
//  if(thisdir.find("2017") != std::string::npos){
//    year = "2017";
//  }
  string year = "2017";


  vector<string> procs = {"zprime"};
  vector<int> nptbins = {7};
  vector<int> nmjjbins = {1};
  vector<double> pass_int = {55456.0, 9501.0, 1421.0, 348.0, 88.0, 29.0, 7.0};
  vector<double> fail_int = {202757.0, 36673.0, 5503.0, 1244.0, 370.0, 126.0, 33.0};

  for(int j=0; j<procs.size(); j++){
    for(int i=0; i<nptbins.at(j); i++){
      for(int k=0; k<nmjjbins.at(j); k++){
	
	TFile* f = new TFile("output/testModel_Datafit.root");
	RooWorkspace* w = (RooWorkspace*)(f->Get("Datafit_ws"));
	RooStats::ModelConfig* mc = (RooStats::ModelConfig*)(w->obj("ModelConfig"));
	
	RooDataSet* data_pass = (RooDataSet*)w->data(("ptbin"+to_string(i)+"pass_data_obs").c_str());
	RooDataSet* data_fail = (RooDataSet*)w->data(("ptbin"+to_string(i)+"fail_data_obs").c_str());
	
	TCanvas *c1 = new TCanvas(("c_"+procs.at(j)+"_"+to_string(i)+to_string(k)).c_str(), 
				  ("c_"+procs.at(j)+"_"+to_string(i)+to_string(k)).c_str(), 600, 600);
	RooPlot* frame1 = (*w->var("msd")).frame(23);

	string bin = "Data_ptbin"+to_string(i);
	cout << bin << endl;

	(*w->pdf(("ptbin"+to_string(i)+"pass_Data").c_str())).plotOn(frame1, LineColor(kRed));

	//data_pass->plotOn(frame1, Rescale(1.0/data_pass->sumEntries()), DataError(RooAbsData::SumW2), MarkerColor(kBlack));
	//data_fail->plotOn(frame1, Rescale(1.0/data_fail->sumEntries()), LineColor(kBlue), MarkerColor(kBlue));
	data_pass->plotOn(frame1, Rescale(1.0/pass_int.at(i)), DataError(RooAbsData::SumW2), MarkerColor(kBlack));
	data_fail->plotOn(frame1, Rescale(1.0/fail_int.at(i)), DataError(RooAbsData::SumW2), LineColor(kBlue), MarkerColor(kBlue));

	/*
 * 	  TH1D* h_pass = (TH1D*)data_pass->createHistogram("data_pass",*w->var("msd"));
 * 	  	  TH1D* h_fail = (TH1D*)data_fail->createHistogram("data_fail",*w->var("msd"));
 * 	  	  	  
 * 	  	  	  	  TH1D* h_ratio = (TH1D*)h_pass->Clone("data_ratio");
 * 	  	  	  	  	  h_ratio->Divide(h_fail);
 * 	  	  	  	  	  	*/
	
	gPad->SetLeftMargin(0.15);
	
	frame1->SetMaximum(0.35);
	frame1->SetMinimum(0);
	
	string title;
	title = "pT Bin "+to_string(100*(i+1))+" to "+to_string(100*(i+2));

	frame1->SetTitle(title.c_str());
	frame1->SetYTitle("Events / 5 GeV");
	frame1->SetXTitle("m_{sd} [GeV]");
	frame1->Draw();
	
	TH1D* h_dum1 = new TH1D("h1","h1",1,0,1);
	TH1D* h_dum2 = new TH1D("h2","h2",1,0,1);
	TH1D* h_dum3 = new TH1D("h3","h3",1,0,1);
	
	h_dum1->SetLineColor(kBlack);
	h_dum1->SetMarkerColor(kBlack);
	h_dum1->SetMarkerStyle(20);
	h_dum2->SetLineColor(kBlue);
	h_dum2->SetMarkerColor(kBlue);
	h_dum2->SetMarkerStyle(20);
	h_dum3->SetLineColor(kRed);
	h_dum3->SetMarkerColor(kRed);
	h_dum3->SetLineWidth(3);
	
	TLegend* leg = new TLegend(0.5,0.7,0.85,0.85);
	leg->SetBorderSize(0);
	leg->AddEntry(h_dum1,"pass","p");
	leg->AddEntry(h_dum2,"fail","p");
	leg->AddEntry(h_dum3,"Fit","l");
	leg->Draw();
	
	//h_ratio->Scale(1.0/h_ratio->Integral());
	//h_ratio->Draw("same");		
	//    cout << (*w->pdf(("ptbin"+to_string(i)+"pass_qcd").c_str())).getNorm() << endl;
	c1->SaveAs(("plots/"+bin+"_fit.png").c_str());
//	c1->SaveAs(("plots/"+bin+"_fit.pdf").c_str());
      }
    }
  }
  
  return 0;

}
