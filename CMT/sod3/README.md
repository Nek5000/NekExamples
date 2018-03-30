# Sod shock tube in 2D.

A diaphragm is initialized at (0,0) in a domain [-1,1] x [0,0.1].

The density ratio across the diaphragm is 8. 

NOTE:
* The highest Courant number I've gotten to work for this case is 0.3.
* The tunable parameter in the EVM, 'c_sub_e' is set to 40.0 in usrdat2.
* The tunable parameter in the EVM, 'c_max' is set to 0.3 in usrdat2.
