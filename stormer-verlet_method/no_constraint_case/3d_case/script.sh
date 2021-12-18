#!/bin/bash
./sv3d 2 3.0 10.0 0.0 10.0 0.5 0.0 dadosProton1Animacao.dat phaseSpaceP1_2.dat
./sv3d 2 3.0 30.0 3.14 10.0 0.5 0.0 dadosProton2Animacao.dat phaseSpaceP2_2.dat
./sv3d 2 3.0 80.0 5.23 10.0 0.5 0.0 dadosProton3Animacao.dat phaseSpaceP3_2.dat
python3 plot3d.py