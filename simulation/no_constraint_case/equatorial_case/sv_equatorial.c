#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M 1.6726219e-27
#define alpha1 3.037e3

//LEMBRAR DE TROCAR O NOME DO ARQUIVO DE SAÍDA!

double effectivePotential(double rho, double c20){
    return (c20*c20)/((2*M*M)*rho*rho) - (alpha1*c20)/(M*rho*rho*rho) + (alpha1*alpha1)/(2*rho*rho*rho*rho);
}

double dVdp(double rho, double c20){
    return (c20*c20)/(M*M)*(1/(rho*rho*rho)) - (c20*3.0*alpha1)/(M)*(1/(rho*rho*rho*rho)) + (2*alpha1*alpha1)/(rho*rho*rho*rho*rho);
}

void polar2cartesian(double *rho, double *drho, double *phi, double dphi, double *x, double *dx, double *y, double *dy, double TAM) {
    for(int n = 0; n<= TAM; n++){

        x[n] = rho[n]*cos(phi[n]);
        dx[n] = drho[n]*cos(phi[n]) - rho[n]*sin(phi[n])*dphi;
        y[n] = rho[n]*sin(phi[n]);
        dy[n] = drho[n]*sin(phi[n]) + rho[n]*cos(phi[n])*dphi;

    }
}

void stormer_verlet_method(double *rho, double *drho, double *phi, double *v_eff, double deltaT, double c20, double TAM) {
    
    for(int n = 1; n<=TAM; n++){
        v_eff[n] = effectivePotential(rho[n-1], c20);
        rho[n] = rho[n-1] + deltaT*drho[n-1] + (deltaT*deltaT*dVdp(rho[n-1], c20))/2;
        drho[n] = drho[n-1] + (deltaT/2)*dVdp(rho[n-1], c20) + (deltaT/2)*dVdp(rho[n], c20);
        phi[n] = phi[n-1] + deltaT*((c20/(M*rho[n-1]*rho[n-1])) - (alpha1/(rho[n-1]*rho[n-1]*rho[n-1])));

    }
}

void getData(char fileParticle[], char filePotential[], double *rho, double *drho, double *phi, double dphi, double *x, double *dx, double *y, double *dy, double *v_eff, double TAM){

    FILE *particle, *effectivePotential;

    particle = fopen(fileParticle, "w");
    effectivePotential = fopen(filePotential, "w");

    fprintf(particle, "n\tx\ty\tz\n");
    fprintf(effectivePotential, "n\tv_eff\trho\n");

    polar2cartesian(rho, drho, phi, dphi, x, dx, y, dy, TAM);
    for(int n = 0; n<=TAM; n++){
        fprintf(particle, "%d %g %g %g\n", n, x[n], y[n], 0.0);
    }

    for(int n = 0; n<=TAM; n++){
        fprintf(effectivePotential, "%d %g %g\n", n, v_eff[n], rho[n]);
    }

    fclose(particle);
    fclose(effectivePotential);
}

int main(int argc, char *argv[]){
    int TAM;
    double *rho, *phi, *drho, dphi, *x, *dx, *y, *dy, *v_eff, deltaT = 0.0001, c20;

    TAM = atof(argv[1])/deltaT;

    rho =  malloc((TAM)*sizeof(double));
    drho =  malloc((TAM)*sizeof(double));
    phi =  malloc((TAM)*sizeof(double));
    x =  malloc((TAM)*sizeof(double));
    dx = malloc((TAM)*sizeof(double));
    y =  malloc((TAM)*sizeof(double));
    dy = malloc((TAM)*sizeof(double));
    v_eff = malloc((TAM)*sizeof(double));

    rho[0] =  atof(argv[2]);
    drho[0] =  atof(argv[3]);
    phi[0] =  atof(argv[4]);
    dphi =  atof(argv[5]); // a derivada de phi é constante.
    c20 = dphi*M*(rho[0]*rho[0]) + M*alpha1*(1/rho[0]);

    stormer_verlet_method(rho, drho, phi, v_eff, deltaT, c20, TAM);

    getData(argv[6], argv[7], rho, drho, phi, dphi, x, dx, y, dy, v_eff, TAM);

    free(rho);
    free(drho);
    free(phi);
    free(x);
    free(dx);
    free(y);
    free(dy);
}