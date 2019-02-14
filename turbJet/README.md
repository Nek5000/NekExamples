# LES of a round turbulent jet
A jet issuing from a pipe with fully developed turbulent flow into a larger
cylindrical domain. The Reynolds number based on the mean (bulk) velocity in 
the pipe and the pipe diameter is 19000. The domain of size D = 10d and
L = 20d, where d is the nozzle diameter is used eliminate the boundary effects.
The inlet boundary extends 1d upstream of the nozzle exit where the velocity
is obtained from another session (turbPipe).

The mesh was generated in Cubit, exported as EXODUSI and storred at ./turbJet/mesh/jet.exo.
Finally it was converted to nek format using ext2nek.

## How to run this example

### Step 1 - Precursor Turbulent Inlet
* cp -a ../turbPipe .
* Run turbPipe for say t=200 to get a fully turbulent pipe flow

### Step 2 - Coupled Simulation
* Restart turbPipe from the saved checkpoint 
* Run the two sessions using e.g. 
```
neknekb_mpmd turbPipe turbJet 4 28 uncoupled
```
* Note, adjust the number of MPI ranks used for each session such that turbJet 
  never waits (check 'data exchange' timings in turbJet.logfile) for the inflow data.
