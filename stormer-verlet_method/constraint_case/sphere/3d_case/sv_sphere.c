#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M 2.0
#define R = 10.0
#define k = 0.5

//LEMBRAR DE TROCAR O NOME DO ARQUIVO DE SAÍDA!
//As variaveis que começam com "d" simbolizam o momento relacionado aquela variável

void spherical2cartesian(   double *theta, 
                            double *dtheta,
                            double *phi,
                            double *dphi,
                            double *x,
                            double *dx,
                            double *y,
                            double *dy,
                            double *z,
                            double *dz,
                            double TAM ) {

         for(int n = 0; n <= TAM; n++){
             //conversao aqui
         }

}

void dHdtheta(){

}

void dHdphi(){

}

void stormer_verlet_method(double *rho, double *drho, double *phi, double *dphi, double *z, double *dz, double deltaT, double TAM) {

    double momentum_theta_aux, momentum_phi_aux;
    
    for(int n = 1; n<=TAM; n++){

        //auxiliares
        
        //coordenadas

        //constante de movimento
    
        //velocidades

    }
}

void getData(char fileParticle[], char filePhaseSpace[], double *theta, double *dtheta, double *phi, double *dphi, double *x, double *dx, double *y, double *dy, double *z, double *dz, double TAM){

    FILE *particle, *phaseSpace;

    particle = fopen(fileParticle, "w");
    phaseSpace = fopen(filePhaseSpace, "w");

    fprintf(particle, "n\tx\ty\tz\n");
    fprintf(phaseSpace, "n\ttheta\tdtheta\n");

    spherical2cartesian(theta, dtheta, phi, dphi, x, dx, y, dy, z, dz, TAM);
    for(int n = 0; n<=TAM; n++){
        fprintf(particle, "%d %g %g %g\n", n, x[n], y[n], z[n]);
    }

    fclose(particle);
    fclose(phaseSpace);
}

int main(int argc, char *argv[]){
    int TAM;
    double *theta, *phi, *dtheta, *dphi, *x, *dx, *y, *dy, *z, *dz, deltaT = 0.0002;

    TAM = atof(argv[1])/deltaT;

    theta =  malloc((TAM)*sizeof(double));
    dtheta=  malloc((TAM)*sizeof(double));
    phi =  malloc((TAM)*sizeof(double));
    dphi = malloc((TAM)*sizeof(double));
    x =  malloc((TAM)*sizeof(double));
    dx = malloc((TAM)*sizeof(double));
    y =  malloc((TAM)*sizeof(double));
    dy = malloc((TAM)*sizeof(double));
    z = malloc((TAM)*sizeof(double));
    dz = malloc((TAM)*sizeof(double));


    theta[0] =  atof(argv[2]);
    dtheta[0] =  M*atof(argv[3]); // momento associado à coord rho
    phi[0] =  atof(argv[4]);
    dphi[0] =  atof(argv[5]); // momento associado à coord phi

    stormer_verlet_method(theta, dtheta, phi, dphi, z, dz, deltaT, TAM);

    getData(argv[6], argv[7], theta, dtheta, phi, dphi, x, dx, y, dy, z, dz, TAM);

    free(theta);
    free(dtheta);
    free(phi);
    free(dphi);
    free(x);
    free(dx);
    free(y);
    free(dy);
    free(z);
    free(dz);
}