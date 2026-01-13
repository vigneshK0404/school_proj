#include <iostream>
#include <stdio.h>
#include "TF1.h"
#include "TCanvas.h"
#include "TApplication.h"
#include "TMath.h"

int main(int argv, char** argc)
{

    Double_t t = 0;

    TF1 f1("f1", "[0]*x^2*exp(-x^2)",-5,5);

    TApplication* app = new TApplication("app",0,0);
    TCanvas c("c","c",1600,800);
    f1.SetMaximum(2);
    f1.SetMinimum(-2);
    f1.Draw();

    while(t < 5000)
    {
        f1.SetParameter(0,TMath::Cos(5*t));
        t += 0.001*TMath::Pi();
        gPad->Modified();
        gPad->Update();
    }
    
    app->Run();
    delete app;

    return 0;
}
