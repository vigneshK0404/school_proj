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

const double pi_inv = 1.0/TMath::Pi();

std::vector<std::vector<double>> waveFunc(std::vector<int> v, std::vector<double> x)
{
    std::vector<std::vector<double>> powerVec;
    std::vector<double> yArr(x.size());
    
    for(size_t i = 0; i < v.size(); ++i)
    {
        double norm = 1.0/sqrt(std::pow(2,v[i]) * TMath::Factorial(v[i]));
        for(size_t j = 0; j < x.size(); ++j)
        {
            yArr[j] =  std::hermite(v[i],x[j]) * std::exp(-(x[j]*x[j]));
            yArr[j] = yArr[j]*norm/std::pow(pi_inv,0.25);
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
    const double upper_bound = 5;
    const double lower_bound = -5;
    const double step_size = (upper_bound - lower_bound) / num_points;
    const double t_max = 500;
    const double o_freq = 1;

    double t = 0;
    double t_step = 1e-3;

    bool first_draw = true;   

    /*****************************************************/

    std::vector<int> powers = {0,1,3}; //ENTER POWERS HERE
    size_t pSize = powers.size();
                                   
    /*****************************************************/

    std::vector<double> xArr(num_points);

    double inputX = lower_bound;
    for(int i = 0; i < num_points; ++i)
    {
        xArr[i] = inputX;
        inputX += step_size;
    } 

    std::vector<std::vector<double>> powerVec = waveFunc(powers,xArr);

    
    TApplication* app = new TApplication("app",0,0);    

    TCanvas c1("c1", "func", 1600,800);
    c1.cd();

    TH1F* frame = gPad->DrawFrame(lower_bound, -5, upper_bound, 5);
    frame->GetXaxis()->SetTitle("x");
    frame->GetYaxis()->SetTitle("Psi(x)");

    TGraph tg(num_points);
    TGraph tg2(num_points);
    tg.SetLineWidth(2);
    tg2.SetLineWidth(2);

    double* x = tg.GetX();
    double* y = tg.GetY();
    double * y2 = tg2.GetY();
    double* x2 = tg2.GetX();

    for(int i = 0; i < num_points; ++i)
    {
        x[i] = xArr[i];
        x2[i] = xArr[i];
    }   

    tg.Draw("L SAME");
    tg2.SetLineColor(kRed);
    tg2.Draw("L SAME");

    gPad->Modified();
    gPad->Update();




    while(t < t_max)
    {
        for(int i = 0; i < num_points; ++i)
        {
            y[i] = 0;
            y2[i] = 0;
        }

        for(size_t p = 0; p < pSize; ++p)
        {
            double omega = o_freq * (powers[p] + 0.5);
            for(size_t k = 0; k < num_points; ++k)
            {
                y[k] += (cos(omega*t) * powerVec[p][k]) / sqrt(pSize);
                y2[k] += y[k]*y[k];
            }
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
    
    delete app;
    
    return 0;
}
