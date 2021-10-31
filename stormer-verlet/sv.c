#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M 1.6726219e-27
#define alpha1 3.037e3

double dVdp(double p, double c20){
    return (c20*c20)/(M*M)*(1/(p*p*p)) - (c20*3.0*alpha1)/(M)*(1/(p*p*p*p)) + (2*alpha1*alpha1)/(p*p*p*p*p);
}

void polar2cartesian(double *rho, double *drho, double *phi, double dphi, double *x, double *dx, double *y, double *dy, double TAM) {
    for(int n = 0; n<= TAM; n++){

        x[n] = rho[n]*cos(phi[n]);
        dx[n] = drho[n]*cos(phi[n]) - rho[n]*sin(phi[n])*dphi;
        y[n] = rho[n]*sin(phi[n]);
        dy[n] = drho[n]*sin(phi[n]) + rho[n]*cos(phi[n])*dphi;

        printf("%d %g %g\n", n, x[n], y[n]);
    }
}

void stormer_verlet_method(double *rho, double *drho, double *phi, double deltaT, double c20, double TAM) {
    
    for(int n = 1; n<=TAM; n++){

        rho[n] = rho[n-1] + deltaT*drho[n-1] + (deltaT*deltaT*dVdp(rho[n-1], c20))/2;
        drho[n] = drho[n-1] + (deltaT/2)*dVdp(rho[n-1], c20) + (deltaT/2)*dVdp(rho[n], c20);
        phi[n] = phi[n-1] + deltaT*((c20/(M*rho[n-1]*rho[n-1])) - (alpha1/(rho[n-1]*rho[n-1]*rho[n-1])));

    }
}

int main(int argc, char *argv[]){
    int TAM;
    double *rho, *phi, *drho, dphi, *x, *dx, *y, *dy, deltaT = 0.001, c20;

    TAM = atof(argv[1])/deltaT;

    rho =  malloc((TAM)*sizeof(double));
    drho =  malloc((TAM)*sizeof(double));
    phi =  malloc((TAM)*sizeof(double));
    x =  malloc((TAM)*sizeof(double));
    dx = malloc((TAM)*sizeof(double));
    y =  malloc((TAM)*sizeof(double));
    dy = malloc((TAM)*sizeof(double));

    rho[0] =  atof(argv[2]);
    drho[0] =  atof(argv[3]);
    phi[0] =  atof(argv[4]);
    dphi =  atof(argv[5]); // a derivada de phi é constante.
    c20 = dphi*M*(rho[0]*rho[0]) + M*alpha1*(1/rho[0]);

    stormer_verlet_method(rho, drho, phi, deltaT, c20, TAM);

    polar2cartesian(rho, drho, phi, dphi, x, dx, y, dy, TAM);

    free(rho);
    free(drho);
    free(phi);
    free(x);
    free(dx);
    free(y);
    free(dy);
}