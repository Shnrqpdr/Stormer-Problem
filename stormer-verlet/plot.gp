set terminal pdf
set output "plotTentativa.pdf"

set title "Stormer-Verlet"
set xlabel "x"
set ylabel "y"
set grid

plot "dadosP1teste.dat" u ($2):($3) w lp ps 0.2 pt 7 lc 6 t "deltaT = 0.000001"

set output