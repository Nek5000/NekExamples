# Pipe flow

This directory contains three pipe cases, where the geometry 
is altered by routine `usrdat2` in the .usr file.

stenosis
helix
cyclic - simulation of bent pipe (torus section) with cyclic bc and
         azimuthal volume forcing

The geometry for "stenosis" was generated by running n2to3, 
which extrudes a 2D mesh into a 3D one.  Once n2to3 is compiled,
one can create this geometry by:

n2to3 < n2to3.in

Then run genmap on the result.  The file n2to3.in can be
modified to suit.

