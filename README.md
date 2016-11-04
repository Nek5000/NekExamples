NekTests
========
Nek unittests
-------------

The NekTests.py module contains the Nek5000 verification tests, implemented 
using the Python standard-library unittest framework.  NekTests requires
Python 2.7 or higher.  

### Module Contents

The module contains a separate class for each test problem.  The classes are:
* Axi
* Benard_Ray9
* Benard_RayDD
* Benard_RayDN
* Benard_RayNN
* Blasius
* ConjHt
* CylRestart_Ca
* CylRestart_Cb
* CylRestart_Pa
* CylRestart_Pb
* Eddy_EddyUv
* Eddy_PsiOmega
* ExtCyl
* Fs2_St1
* Fs2_St2
* Fs2_StdWv
* FsHydro
* Hemi
* Kovasznay
* KovStState
* LowMachTest
* Mhd_Gpf
* Mhd_GpfB
* Mhd_GpfM
* Os7000
* Peris
* Pipe_Helix
* Pipe_Stenosis
* Rayleigh_Ray1
* Rayleigh_Ray2
* Shear4_Shear4
* Shear4_Thin
* Solid
* Strat_P0001
* Strat_P1000
* Taylor
* ThreeDBox
* TurbChannel
* VarVis
* Vortex
* Vortex2

Each class also contains four methods for different formulations and
parallelization modes:
* test_PnPn_Serial
* test_PnPn_Parallel
* test_PnPn2_Serial
* test_PnPn2_Parallel

### Running Tests

The tests may be run using the Python standard-library 'unittest' module, which
requires no additional dependencies.  The tests may also be run with any
third-party testing tool compatible with unittest, such as nose, py.test,
TwistedTrial, and others.  

#### Setting Up Your Environment

Before running the tests, these environment variables should be defined:

* `SOURCE_ROOT`: Points to the top-level Nek5000 repository. (default: none)
* `CC`: The C compiler you wish to use. (default: gcc)
* `F77`: The Fortran 77 compiler you wish to use. (default gfortran)
* `IFMPI=[true|false]`: If true, run tests with MPI. (default: false)

These environment variables may optionally be defined:
* `EXAMPLES_ROOT`: Points to an alternate Nek5000 examples directory.  For
   example, `$HOME/NekExamples`. (default: this directory)
* `TOOLS_ROOT`: Points to an alternate directory for Nek5000 tools. (default:
   `$SOURCE_ROOT/tools`)
* `SCRIPTS_ROOT`: Points to an alternate directory Nek5000 scripts directory. 
* `TOOLS_BIN`: If defined, compile tools in this directory. (default: `$SOURCE_ROOT/bin`)
* `LOG_ROOT`: If defined, move completed logs into this directory.  If not defined,
  leave logs in the example folders.  (default: undefined)
* `VERBOSE_TESTS=[true|false]`: If true, display standard output from compiler and
   Nek5000 to terminal window.  Standard output will always be recorded in
   logfiles, whether VERBOSE_TESTS is true or false.  (default: true)
* `PARALLEL_PROCS`: The number of processes to use when running with MPI.
  (default: 4)

#### Running NekTests with unittest

To run all the tests, first `cd` into this directory and then run:
`$ python -m 'unittest' NekTests`

If you wish to run tests for just one example problem (for example, "TurbChannel"), run:
`$ python -m 'unittest' NekTests.TurbChannel`

If you wish to run tests for just one example problem and one
formulation/parallelization (for example, test_PnPn_Serial), run:
`$ python -m 'unittest' NekTests.TurbChannel.test_PnPn_Serial`
