This case is identical to the CHT case. But it runs with a "frozen"
velocity (no velocity solve) and the heat load is unsteady. 

The heat load is sinusoidal and the parameters can be controlled
through the par file.

In addition temperature is solved with Helmholtz (stored in temp)
and CVODE (stored in scalar 01). Grep output for 'terr' to get
deviation.  
