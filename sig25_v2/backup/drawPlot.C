/************************************************
 *  * Jennet Dickinson 
 *   * Nov 19, 2020
 *    * Draw Roofit plots
 *     ************************************************/
#include <iostream>
#include <string>

using namespace RooFit;
using namespace RooStats;
using namespace std;

//gROOT.SetBatch(True);

void drawPlot(){

//	TFile* f = TFile::Open("fitDiagnosticsTest.root");

	//PF Ratio
	double pfratio = 0.2690730356705518;

	gStyle->SetOptStat(0);

        TFile* f = new TFile("fitDiagnosticsTest.root");
	
	RooPlot *h = (RooPlot*)f->Get("ptbin0pass_msd_fit_b");
	auto *atest = (TGraph*)(h->getObject(0));
	auto *btest = (RooCurve*)(h->getObject(1));
	TH1F *datatest = new TH1F("datatest", "Data", 40, 0, 200);
	datatest->SetLineColor(kBlack);
	TH1F *fittest = new TH1F("fittest", "Fit", 40, 0, 200);
	fittest->SetLineColor(kBlue);
	double xt1=0;
	double yt1=0;
	double xt2=0;
	double yt2=0;
	for(int k=0; k<41; k++){
		atest->GetPoint(k, xt1, yt1);
		cout << "Data xPoint:"+to_string(xt1)<<endl;
		cout << "Data yPoint:"+to_string(yt1)<<endl;
		datatest->Fill(xt1,yt1);
		btest->GetPoint(2*k+3, xt2, yt2);
		cout << "Fit xPoint:"+to_string(xt1)<<endl;
		cout << "Fit yPoint:"+to_string(yt2)<<endl;
		fittest->Fill(xt1,yt2);
	}
	TCanvas c0;
	c0.cd();		
	
	datatest->SetMarkerStyle(kFullCircle);
	fittest->SetLineWidth(3);
	datatest->SetLineWidth(3);

	datatest->Draw("hist P");
	fittest->Draw("same hist");

	TLegend *l0 = new TLegend(.6, .75, .9, .9);
	l0->AddEntry(datatest, "Data");
	l0->AddEntry(fittest, "Fit");
	l0->Draw();
	
	c0.SaveAs("./Test_FitPlot_v2.png");
	
	
	TH1F *data = new TH1F("data", "Data", 40, 0, 200);
	data->SetLineColor(kBlack);
	TH1F *fit = new TH1F("fit", "Fit", 40, 0, 200);
	fit->SetLineColor(kBlue);
	double x1=0;
	double y1=0;
	double x2=0;
	double y2=0;

	char *n;

	TGraph *a;
	TGraph *b;

	for(int j=0; j<38; j++){
		string str = "ptbin"+to_string(j)+"pass_msd_fit_b";
		n = const_cast<char*>(str.c_str());
		
		cout << n << endl;

		RooPlot *c = (RooPlot*)f->Get(n);
		
		a =  (TGraph*)(c->getObject(0));
		b =  (TGraph*)(c->getObject(1));
		//TGraph *a = new (TGraph*)(f->Get("ptbin"+to_string(j)+"pass_msd_fit_b")->getObject(0));
		//TGraph *b = new (TGraph*)(f->Get("ptbin"+to_string(j)+"pass_msd_fit_b")->getObject(1));
		
		for(int k=0; k<41; k++){
//			x = a->GetPointX(k);
//			y = a->GetPointY(k);
			a->GetPoint(k, x1, y1);
			data->Fill(x2,y2);
//			x = b->GetPointX(k);
//			y = b->GetPointY(k);
			b->GetPoint(2*k+3, x2, y2);
			fit->Fill(x1,y2);
			
			
		}		
	}	
	TCanvas c1;
	c1.cd();
	
	data->SetMarkerStyle(kFullCircle);
	fit->SetLineWidth(3);
	data->SetLineWidth(3);

	data->Draw("hist P");
	fit->Draw("same hist");
	

	TLegend *l1 = new TLegend(.6, .75, .9, .9);
	l1->AddEntry(data, "Data");
	l1->AddEntry(fit, "Fit");
	l1->Draw();
	
	c1.SaveAs("./Total_FitPlot_v2.png");
	
  
  return 0;

}
