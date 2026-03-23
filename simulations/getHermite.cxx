Double_t getWF(Int_t n, Double_t x)
{
    Double_t herm_base[2] = {1,2*x};
    Double_t herm = 0;

    if(n == 0 || n == 1){return herm_base[n];}

    for(int i = 2; i < n+1; ++i)
    {
        herm = 2*x*herm_base[(i+1)%2] - 2*(i-1)*herm_base[(i)%2] //* Q_rsqrt(fac * expo) * std::exp(-x*x);
        herm_base[i%2] = herm
    }

    return herm;
}

