#!/bin/bash

for ((drho = 0; drho <= 85; drho++))
do
    ./sv3d 2 3.0 $drho 0.0 10.0 0.5 0.5 non.dat phaseSpaceProton$drho.dat
done
