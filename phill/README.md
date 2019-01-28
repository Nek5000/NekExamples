# 3D PERIODIC HILL

This example is similar to the one presented in Nek5000 documentation, however
the hill profile is consistent with Almeida et al. 1993 and described at
https://turbmodels.larc.nasa.gov/Other_LES_Data/2Dhill_periodic/hill-geometry.dat

HOW TO RUN THE CASE
1. Compile the code
2. Build the initial box mesh using genbox and phill.box -> box.re2
3. cp box.re2 phill.re2
4. genmap on phill.re2
5. Check phill.par and run the simulation
5. The mesh of the periodic hill is saved as newre2.re2

REMARKS:
- phill.re2 is a rectangular channel
- the geometric parameters of the hill are defined in userdat2
- it is assumed that the Reynolds number is based on the average velocity
  over the inlet plane
