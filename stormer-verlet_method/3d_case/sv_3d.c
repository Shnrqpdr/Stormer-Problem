#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M 1.6726219e-27
#define alpha1 3.037e3

//LEMBRAR DE TROCAR O NOME DO ARQUIVO DE SAÍDA!

/*double effectivePotential(double rho, double c20){
    return (c20*c20)/((2*M*M)*rho*rho) - (alpha1*c20)/(M*rho*rho*rho) + (alpha1*alpha1)/(2*rho*rho*rho*rho);
}*/

double dHdp(double rho, double z, double c2){

    double R = sqrt(rho*rho + z*z);
    double expression = - (c2*c2/(M*rho*rho*rho)) - 3*((M*alpha1*alpha1*rho*rho*rho)/(R*R*R*R*R*R*R*R)) + ((M*alpha1*alpha1*rho)/(R*R*R*R*R*R)) + (3*alpha1*c2*rho)/(R*R*R*R*R);

    return expression;
}

double dHdz(double rho, double z, double c2){

    double R = sqrt(rho*rho + z*z);
    double expression = - (3*M*alpha1*alpha1)*((rho*rho*z)/(R*R*R*R*R*R*R*R)) + (3*alpha1*c2)*((z)/(R*R*R*R*R));

    return expression;
}

void polar2cartesian(double *rho, double *drho, double *phi, double dphi, double *x, double *dx, double *y, double *dy, double TAM) {
    for(int n = 0; n<= TAM; n++){

        x[n] = rho[n]*cos(phi[n]);
        dx[n] = drho[n]*cos(phi[n]) - rho[n]*sin(phi[n])*dphi;
        y[n] = rho[n]*sin(phi[n]);
        dy[n] = drho[n]*sin(phi[n]) + rho[n]*cos(phi[n])*dphi;
    }
}

void stormer_verlet_method(double *rho, double *drho, double *phi, double dphi, double *z, double *dz, double *v_eff, double deltaT, double *c2, double TAM) {

    double momentum_rho_aux, momentum_dz_aux;
    
    for(int n = 1; n<=TAM; n++){

        //auxiliares
        momentum_rho_aux = drho[n-1] - deltaT*dHdp(rho[n-1], z[n-1], c2[0]); // 
        momentum_dz_aux = dz[n-1] - deltaT*dHdz(rho[n-1], z[n-1], c2[0]);
        
        //coordenadas
        rho[n] = rho[n-1] +  deltaT*(momentum_rho_aux/M);
        z[n] = z[n-1] + deltaT*(momentum_dz_aux/M);
        phi[n] = phi[n-1] + deltaT*((c2[0])/(M*rho[n-1]*rho[n-1]) - (alpha1/(sqrt(rho[n-1]*rho[n-1] + z[n-1]*z[n-1])*sqrt(rho[n-1]*rho[n-1] + z[n-1]*z[n-1])*sqrt(rho[n-1]*rho[n-1] + z[n-1]*z[n-1]))));

        //constante de movimento
        //c2[n] = M*rho[n]*rho[n]*dphi + (M*alpha1*rho[n]*rho[n])/(sqrt(rho[n]*rho[n] + z[n]*z[n])*sqrt(rho[n]*rho[n] + z[n]*z[n])*sqrt(rho[n]*rho[n] + z[n]*z[n]));

        //velocidades
        drho[n] = momentum_rho_aux - deltaT*dHdp(rho[n], z[n], c2[0]);
        dz[n] = momentum_dz_aux - deltaT*dHdz(rho[n], z[n], c2[0]);

    }
}

void getData(char fileParticle[], char filePhaseSpace[], double *rho, double *drho, double *phi, double dphi, double *x, double *dx, double *y, double *dy, double *z, double *dz, double *v_eff, double TAM){

    FILE *particle, *phaseSpace;

    particle = fopen(fileParticle, "w");
    phaseSpace = fopen(filePhaseSpace, "w");

    fprintf(particle, "n\tx\ty\tz\n");
    fprintf(phaseSpace, "n\trho\tdrho\n");

    polar2cartesian(rho, drho, phi, dphi, x, dx, y, dy, TAM);
    for(int n = 0; n<=TAM; n++){
        fprintf(particle, "%d %g %g %g\n", n, x[n], y[n], z[n]);
    }

    for(int n = 0; n<=TAM; n++){
        fprintf(phaseSpace, "%d %g %g\n", n, rho[n], drho[n]/M);
    }

    fclose(particle);
    fclose(phaseSpace);
}

int main(int argc, char *argv[]){
    int TAM;
    double *rho, *phi, *drho, dphi, *x, *dx, *y, *dy, *z, *dz, *v_eff, *c2, deltaT = 0.0002, c20;

    TAM = atof(argv[1])/deltaT;

    rho =  malloc((TAM)*sizeof(double));
    drho =  malloc((TAM)*sizeof(double));
    phi =  malloc((TAM)*sizeof(double));
    x =  malloc((TAM)*sizeof(double));
    dx = malloc((TAM)*sizeof(double));
    y =  malloc((TAM)*sizeof(double));
    dy = malloc((TAM)*sizeof(double));
    z = malloc((TAM)*sizeof(double));
    dz = malloc((TAM)*sizeof(double));
    v_eff = malloc((TAM)*sizeof(double));
    c2 = malloc((TAM)*sizeof(double));

    rho[0] =  atof(argv[2]);
    drho[0] =  M*atof(argv[3]); // momento associado à coord rho
    phi[0] =  atof(argv[4]);
    dphi =  atof(argv[5]); // a derivada de phi é constante.
    z[0] = atof(argv[6]);
    dz[0] = M*atof(argv[7]); // momento associado à coord z
    c2[0] = M*rho[0]*rho[0]*dphi + (M*alpha1*rho[0]*rho[0])/(sqrt(rho[0]*rho[0] + z[0]*z[0])*sqrt(rho[0]*rho[0] + z[0]*z[0])*sqrt(rho[0]*rho[0] + z[0]*z[0]));

    printf("\n%g\n", c2[0]);
    stormer_verlet_method(rho, drho, phi, dphi, z, dz, v_eff, deltaT, c2, TAM);

    getData(argv[8], argv[9], rho, drho, phi, dphi, x, dx, y, dy, z, dz, v_eff, TAM);

    free(rho);
    free(drho);
    free(phi);
    free(x);
    free(dx);
    free(y);
    free(dy);
    free(v_eff);
    free(z);
    free(dz);
    free(c2);
}