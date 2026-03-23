#include <iostream>
#include <SFML/Graphics.hpp>
#include <vector>
#include <cmath>
#include <algorithm>


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

    std::cout << "Radii Size: " << Radii.size() << "\n";
    
    ProbDensity(n,l,m,Radii,Thetas,psi);

    double maxProb = *max_element(psi.begin(),psi.end());
    
    std::cout << maxProb << std::endl;
    


    /*sf::RenderWindow window(sf::VideoMode({200, 200}), "SFML works!");
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);

    while (window.isOpen())
    {
        while (const std::optional event = window.pollEvent())
        {
            if (event->is<sf::Event::Closed>())
                window.close();
        }

        window.clear();
        window.draw(shape);
        window.display();
    }*/
}
