#include <iostream>
#include <stdio.h>
#include <cmath>
#include "TCanvas.h"
#include "TApplication.h"
#include "TGraph.h"
#include "TH1F.h"
#include "TSystem.h"
#include <vector>

double waveFunc(std::vector<int> v, double x)
{
    double h = 0;
    for(size_t i = 0; i < v.size(); ++i)
    {
        h += std::hermite(v[i],x) * std::exp(-(x*x));
    }
   return h;
}
int main(int argc, char** argv)
{
    const int num_points = 1000;
    const double upper_bound = 5;
    const double lower_bound = -5;
    const double step_size = (upper_bound - lower_bound) / num_points;
    const double t_max = 500;

    double t = 0;
    double t_step = 1e-3;

    bool first_draw = true;    

    TApplication* app = new TApplication("app",0,0);    

    TCanvas c1("c1", "func", 1600,800);
    c1.cd();

    TH1F* frame = gPad->DrawFrame(lower_bound, -2.0, upper_bound, 2.0);
    frame->GetXaxis()->SetTitle("x");
    frame->GetYaxis()->SetTitle("Psi(x)");

    TGraph tg(num_points);
    tg.SetLineWidth(2);

    double* x = tg.GetX();
    double* y = tg.GetY();

    double* yArr = new double[num_points];

    std::vector<int> powers = {0,1,2};

    double inputX = lower_bound;
    for(int i = 0; i < num_points; ++i)
    {
        x[i] = inputX;
        yArr[i] = waveFunc(powers,inputX);
        inputX += step_size;
    } 


    tg.Draw("L SAME");

    gPad->Modified();
    gPad->Update();


    while(t < t_max)
    {
        for(int i = 0; i < num_points; ++i)
        {
            y[i] = cos(t)*yArr[i];
        }

        
        if(static_cast<int>(t*1000) % 10 ==0)
        {
            gPad->Modified();
            gPad->Update();
            gSystem->ProcessEvents();
        }   

        t += t_step;

    }

    app->Run();    
    
    delete app,x,y,yArr;
    
    return 0;
}
