# Helical Forcing Dynamo.

This example gives a cicular Polarized Flow of Galloway & Proctor [1]. 
Magnetic field growth rate (or 1/2 of magnetic energy growth rate)
is equal to ~ 0.3  for K_z=0.57 at Rm=100 (magnetic Reynolds #)

Note: magnetic field growth rate (or 1/2 of magnetic energy growth
rate) is equal to ~ 0.26  for K_z=0.57 at Rm=10 (CKPT95)

Files:
        gpf.*		Base case (Re=Rm=10)
        gpf_re.rea	Case  w/ Re=Rm=100

## MHD:

For an MHD case, B-field is stored after temperature array
(and passive scalars if any) so ldimt>=2.  Note that in all routines
w/ NEKUSE common block i.e. uservp, userf, userq, userbc & useric,
B-field can be accessed through ux,uy,uz when
they are called with ifield=ifldmhd (ifield=1 is for velocity,
ifield=2 for temperature or ifield=ifldmhd=2 when IFHEAT=.FALSE.,
etc.) in addition to the direct reference bx(ix,iy,iz,ieg),
by(ix,iy,iz,ieg), etc.
Also  note that a call to outpost in userchk enforces B-field dump
in odd numbers of .f/.fld files in place of velocity. Then for
restart, one has to provide two files in .rea file -- first,
velocity .f/.fld (even number) file name and on the next line, a
file name of the B-field dump (odd .f/.fld number) both preceeded
with a line

      2 PRESOLVE/RESTART OPTIONS

A major limitation of the current version of MHD implementation,
is the requirement that the boundary conditions for magnetic field 
have to be of the same type as for velocity  field, e.g.,
both periodic ('PER'), Direchlet ('v  '), etc.
Also ioinfo control and avg_all routine do not have a support 
for magnetic field yet.
