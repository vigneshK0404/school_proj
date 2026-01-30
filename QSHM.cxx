#include <iostream>
#include <stdio.h>
#include <cmath>
#include "TCanvas.h"
#include "TApplication.h"
#include "TGraph.h"
#include "TH1F.h"
#include "TSystem.h"
#include <vector>
#include <algorithm>
#include "TMath.h"
#include "TLegend.h"

const Double_t pi_inv = std::pow(1.0/TMath::Pi(),0.25);

Double_t getWF(Int_t n, Double_t x)
{
    Double_t exp_term = std::exp(-0.5*x*x);
    Double_t WF_base[2] = {pi_inv* exp_term, sqrt(2)*pi_inv*x*exp_term};
    Double_t WF = 0;

    if(n == 0 || n == 1){return WF_base[n];}

    for(int i = 2; i < n+1; ++i)
    {
        WF = x*sqrt(2.0/(i+1))*WF_base[(i+1)%2] - sqrt(i/(i+1.0))*WF_base[(i)%2]; 
        WF_base[i%2] = WF;
    }

    return WF;
}


std::vector<std::vector<Double_t>> waveFunc(std::vector<Int_t> v, std::vector<Double_t> x)
{
    std::vector<std::vector<Double_t>> powerVec;
    powerVec.reserve(v.size());
    std::vector<Double_t> yArr(x.size());
    
    for(size_t i = 0; i < v.size(); ++i)
    {
        for(size_t j = 0; j < x.size(); ++j)
        {
            yArr[j] =  getWF(v[i],x[j]);
            //printf("%f\n",yArr[j]);

        }
        //std::cout << std::endl;

        powerVec.push_back(yArr);
    }
   return powerVec;
}
int main(int argc, char** argv)
{
    const int num_points = 500;
    const Double_t upper_bound = 5;
    const Double_t lower_bound = -5;
    const Double_t step_size = (upper_bound - lower_bound) / num_points;
    const Double_t t_max = 500;
    const Double_t o_freq = 1;

    Double_t t = 0;
    Double_t t_step = 1e-3;

    bool first_draw = true;   

    /*****************************************************/

    std::vector<int> powers = {0,1,static_cast<int>(1e6)}; //ENTER POWERS HERE
    size_t pSize = powers.size();
                                   
    /*****************************************************/

    std::vector<Double_t> xArr(num_points);

    Double_t inputX = lower_bound;
    for(int i = 0; i < num_points; ++i)
    {
        xArr[i] = inputX;
        inputX += step_size;
    } 

    std::vector<std::vector<Double_t>> powerVec = waveFunc(powers,xArr);
    
    Double_t max_el = -5;
    Double_t min_el = 1e10;
    for(int s = 0; s < powerVec.size(); ++s)
    {
        Double_t max = *std::max_element(powerVec[s].begin(), powerVec[s].end());
        Double_t min = *std::min_element(powerVec[s].begin(), powerVec[s].end());
        max_el = (max > max_el ? max : max_el);
        min_el = (min < min_el ? min : min_el);
    }

    max_el += 0.8;
    min_el -= 0.8;


    
    TApplication* app = new TApplication("app",0,0);    
    auto* legend = new TLegend(0.75, 0.75, 0.9, 0.9);

    TCanvas c1("c1", "func", 1600,800);
    c1.cd();

    TH1F* frame = gPad->DrawFrame(lower_bound, min_el, upper_bound, max_el);
    frame->GetXaxis()->SetTitle("x");
    frame->GetYaxis()->SetTitle("Psi(x)");

    TGraph tg(num_points);
    TGraph tg2(num_points);
    tg.SetLineWidth(2);
    tg2.SetLineWidth(2);

    Double_t* x = tg.GetX();
    Double_t* y = tg.GetY();
    Double_t * y2 = tg2.GetY();
    Double_t* x2 = tg2.GetX();

    for(int i = 0; i < num_points; ++i)
    {
        x[i] = xArr[i];
        x2[i] = xArr[i];
    }   

    tg.Draw("L SAME");
    tg2.SetLineColor(kRed);
    tg2.Draw("L SAME");

    legend->AddEntry(&tg, "WaveFunction");
    legend->AddEntry(&tg2, "Prob Density");
    legend->Draw();
   
    gPad->Modified();
    gPad->Update();

    while(t < t_max)
    {
        for(int i = 0; i < num_points; ++i)
        {
            y[i] = 0;
            y2[i] = 0;
        }

        for(size_t k = 0; k < num_points; ++k)
        {
            for(size_t p = 0; p < pSize; ++p)
            {
                Double_t omega = o_freq * (powers[p] + 0.5);
                y[k] += (cos(omega*t) * powerVec[p][k]) / sqrt(pSize); 
            }
            y2[k] = y[k]*y[k];

        //TODO : FIX Prob density it is not accounting for cross terms right now

        }
        
        if(static_cast<int>(t*1000) % 100 ==0)
        {
            gPad->Modified();
            gPad->Update();
            gSystem->ProcessEvents();
        }   

        t += t_step;

    }

    app->Run();    
    
    delete app,legend;
    
    return 0;
}
