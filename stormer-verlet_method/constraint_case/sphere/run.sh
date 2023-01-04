#!/bin/bash
gcc -o sv sv_sphere.c -lm
./sv 30 1.308996939 0.0 0.0 -0.394 data/sphere.dat data/phase_space.dat
python3 plotSphere.py