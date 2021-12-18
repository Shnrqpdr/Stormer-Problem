#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M 2.0
#define R 10.0
#define k 0.5

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

            // coordenadas

            x[n] = R*cos(phi[n])*sin(theta[n]);
            y[n] = R*sin(phi[n])*sin(theta[n]);
            z[n] = R*cos(theta[n]);

            //momentos

            dx[n] = 0;
            dy[n] = 0;
            dz[n] = 0;
        }
}

double dHd_theta(double theta, double dtheta, double phi, double dphi){

    double Lz = M*R*R*dphi*sin(theta)*sin(theta);

    double expression = - (Lz*Lz)/(M*R*R*sin(theta)*sin(theta)*tan(theta)) + (Lz*k*sin(2*theta))/(M*R*R*sin(theta)*sin(theta));

    return expression;
}

double dHd_dtheta(double theta, double dtheta, double phi, double dphi){

    double expression = dtheta/(M*R*R);

    return expression;
}

double dHd_phi(double theta, double dtheta, double phi, double dphi){

    double expression = 0;

    return expression;
}

double dHd_dphi(double theta, double dtheta, double phi, double dphi){

    double Lz = M*R*R*dphi*sin(theta)*sin(theta);

    double expression = (Lz)/(M*R*R*sin(theta)*sin(theta));

    return expression;

}

void stormer_verlet_method(double *theta, double *dtheta, double *phi, double *dphi, double deltaT, double TAM) {

    double momentum_theta_aux, momentum_phi_aux;
    
    for(int n = 1; n<=TAM; n++){

        //auxiliares
        momentum_theta_aux = dtheta[n-1] - deltaT*dHd_theta(theta[n-1], dtheta[n-1], phi[n-1], dphi[n-1]);
        momentum_phi_aux = dphi[n-1] - deltaT*dHd_phi(theta[n-1], dtheta[n-1], phi[n-1], dphi[n-1]);
        
        //coordenadas
        theta[n] = theta[n-1] + deltaT*dHd_dtheta(theta[n-1], momentum_theta_aux, phi[n-1], dphi[n-1]);
        phi[n] = phi[n-1] + deltaT*dHd_dphi(theta[n-1], momentum_theta_aux, phi[n-1], momentum_phi_aux);

        //constante de movimento
    
        //velocidades
        dtheta[n] = momentum_theta_aux - deltaT*dHd_theta(theta[n], dtheta[n-1], phi[n], dphi[n-1]);
        dphi[n] = momentum_phi_aux - deltaT*dHd_phi(theta[n], dtheta[n-1], phi[n], dphi[n-1]);
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

    stormer_verlet_method(theta, dtheta, phi, dphi, deltaT, TAM);

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