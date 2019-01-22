# Kovasznay flow: flow behind a two-dimensional grid

This flow is an analytical, two-dimensional, steady solution to the incompressible Navier-Stokes equations.
As the analytical solution exists, this test can be used to demonstrates spectral convergence of the Kovasznay 
solution for the case of PN-PN. (Easily changed to PN-PN-2, by editing SIZE and setting lx2=lx1-2). The error 
printed in the log file consists essentially of different norms of the velocity error.

The results for Pn-PN should look something like (N- polynomial order):

%nstep  N      Err 1       Err 2        Err 3        Err 4      final time
 15000  3  3.80564E-01  2.25192E-01  1.73472E-02  3.30967E-02  1.50000E+01 err
 15000  4  9.60456E-02  5.68423E-02  4.03567E-03  8.27257E-03  1.50000E+01 err
 15000  5  6.33196E-03  3.74929E-03  1.75654E-04  4.90411E-04  1.50000E+01 err
 15000  6  1.78099E-03  1.05473E-03  3.78376E-05  1.29057E-04  1.50000E+01 err
 15000  7  9.33791E-05  5.53076E-05  1.31083E-06  7.20706E-06  1.50000E+01 err
 15000  8  1.93170E-05  1.14416E-05  2.23850E-07  1.32963E-06  1.50000E+01 err
 15000  9  1.01962E-06  6.03945E-07  9.72991E-09  7.20755E-08  1.50000E+01 err
 15000 10  1.36397E-07  8.07892E-08  1.57699E-09  7.18209E-09  1.50000E+01 err
 15000 11  1.75185E-08  1.03638E-08  8.86536E-10  2.05708E-09  1.50000E+01 err
 15000 12  1.94871E-08  1.15182E-08  1.28181E-09  2.53149E-09  1.50000E+01 err
 15000 13  2.20911E-08  1.30527E-08  1.56650E-09  2.99709E-09  1.50000E+01 err
 15000 14  2.56139E-08  1.51300E-08  1.91387E-09  3.74751E-09  1.50000E+01 err
 15000 15  1.14514E-08  6.78022E-09  3.42498E-10  9.69512E-10  1.50000E+01 err
