#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>


struct particle
{
    double r;
    double t;
    double p;
    particle(double r, double t, double p) : r(r) , t(t), p(p) {}
};


void ProbDensity(unsigned int n, unsigned int l, unsigned int m ,
        const std::vector<double>& r, const std::vector<double>& theta, 
        std::vector<double>& psi)
{  
    //std::cout << "Entry\n";
    psi.clear();
    psi.reserve(r.size() * theta.size());
    
    double Norm = 2*std::sqrt(std::tgamma(n-l)/(std::pow(n,4)*std::tgamma(n+l+1)));
    //std::cout << "size() & Norm: " << psi.size() << " " << Norm <<"\n";

    for(const double& R : r)
    {
        double rho = 2.0 *R /n;
        double Lag = std::assoc_laguerre(n-l-1, (2*l)+1, rho);
        double radialPart = Norm*std::exp(-rho/2)*std::pow(rho,l)*Lag;
        //std::cout << "NEW RADIUS\n";
        for(const double& T : theta)
        {
            double wf = radialPart*std::sph_legendre(l,m,T);
            double prob = wf*wf;
            //std::cout << prob << "\n";
            psi.push_back(prob);
        }
    }
    //std::cout << "Check3\n";


    return;
}


std::vector<double> generateSpace(double min, double max, double steps)
{
    std::vector<double> v;
    v.reserve(steps);
    double stepSize = (max - min)/steps;
    for(size_t i = 0; i < steps; ++i)
    {
        v.push_back(min + i*stepSize);
        //std::cout << v[i] << "\n";
    }

    return v;    
}


int main()
{
    unsigned int n = 1;
    unsigned int l = 0;
    unsigned int m = 0;

    double minR = 0;
    double maxR = 10;

    double minT = 0;
    double maxT = M_PI;

    double minP = 0;
    double maxP = 2*M_PI;


    std::vector<double> Radii = generateSpace(minR,maxR,100);
    std::vector<double> Thetas = generateSpace(minT,maxT,100);
    std::vector<double> Phis = generateSpace(minP,maxP,100);
            
    std::vector<double> psi;

    //std::cout << "Radii Size: " << Radii.size() << "\n";
    
    ProbDensity(n,l,m,Radii,Thetas,psi);

    double maxProb = *max_element(psi.begin(),psi.end());
    
    std::random_device rd; // obtain a random number from hardware
    std::mt19937 gen(rd()); // seed the generator

    std::uniform_real_distribution<> coverDist(0,1.0);

    double RadDistH = 1/(maxR-minR);
    double ThetaDistH = 1/(maxT-minT);

    double coverProb = maxProb * RadDistH * ThetaDistH;


    std::vector<particle> particleVec;
    size_t Tsize = Thetas.size();

    for(size_t i = 0; i < Radii.size(); ++i)
    {
        for(size_t j = 0; j < Thetas.size(); ++j)
        {
            size_t idx = i*Tsize + j;
            double probRatio = psi[idx]/coverProb;
            double headFlip = coverDist(gen);

            if(probRatio <= headFlip)
            {
                for(size_t k = 0; k < Phis.size(); ++k)
                {
                    particleVec.emplace_back(Radii[i],Thetas[j],Phis[k]);

                }

            }
        }
    }


    std::cout << particleVec.size() << std::endl;


        
}
