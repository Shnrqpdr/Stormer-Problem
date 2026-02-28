#!/bin/bash
# Parâmetros: tempo_total theta0 p_theta0 phi0 p_phi arquivo_saída_partícula arquivo_fase
# Artigo: M=2, R=10, k=0.5 (unidades arbitrárias)
gcc -o sv sv_sphere.c -lm

# Figura 6(a): theta0=pi/4, p_theta0=0, p_phi=0.394
# ./sv 30 0.785398163 0.0 0.0 0.394 data/sphere.dat data/phase_space.dat

# Figura 6(b): theta0=pi/3, p_theta0=0, p_phi=0.394
./sv 3000 1.047197551 0.0 0.0 0.394 data/sphere.dat data/phase_space.dat

python3 plotSphere.py sphere_plot_fig6b.png

# Figura 6(c): theta0=75°=75*pi/180, p_theta0=0, p_phi=-0.394
./sv 3000 1.308996939 0.0 0.0 -0.394 data/sphere.dat data/phase_space.dat

python3 plotSphere.py sphere_plot_fig6c.png

# Figura 7(a): theta0=0.6 rad, p_phi=0.5*k=0.25, p_theta0=0.1 (hemisfério norte)
./sv 3000 0.6 0.1 0.0 0.25 data/sphere.dat data/phase_space.dat

python3 plotSphere.py sphere_plot_fig7a.png

# Figura 7(b): limite equatorial, p_theta0=0.191725
./sv 3000 0.6 0.191725 0.0 0.25 data/sphere.dat data/phase_space.dat

python3 plotSphere.py sphere_plot_fig7b.png

# Figura 7(c): cruza equador, p_theta0=0.2525
./sv 3000 0.6 0.2525 0.0 0.25 data/sphere.dat data/phase_space.dat

python3 plotSphere.py sphere_plot_fig7c.png

# Padrão: Figura 6(a)
./sv 3000 0.785398163 0.0 0.0 0.394 data/sphere.dat data/phase_space.dat

python3 plotSphere.py sphere_plot_fig6a.png