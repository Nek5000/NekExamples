NekTests
========
Nek unittests
-------------

The NekUnitTests.py module contains the Nek5000 verification tests, implmented 
using the Python standard-library unittests framework.  The modules require 
Python 2.7 or higher.  

### Module Contents

The module contains the following classes and methods (listed as items and 
subitems,  respectively):

* TurbChannelPnPn
  * test_GmresSerial
* TurbChannelPnPn2
  * test_GmresSerial

### Running Tests

The tests may be run standalone (using only Python standard-library packages) or 
through a variety of third-party tools (nose, pytest, etc).  A few methods are 
described here.  

#### Environment

Before using any method below, three environment variables must be defined:

* `SOURCE_ROOT`: points to the Nek5000 source directory (for example, 
  `$HOME/nek5_svn/trunk/nek`)
* `TOOLS_ROOT`: points to the Nek5000 tools directory (for example,
  `$HOME/nek5_svn/trunk/tools`)
* `EXAMPLES_ROOT`: points to the Nek5000 examples directory (for example,
  `$HOME/nek5_svn/examples`)
  
These can be defined in several ways.  On the command line, you can use:
```
$ export SOURCE_ROOT=$HOME/nek5_svn/trunk/nek
$ export TOOLS_ROOT=$HOME/nek5_svn/trunk/tools
$ export EXAMPLES_ROOT=$HOME/nek5_svn/examples
$ python3 NekUnitTests.py
```
or :
```
$ SOURCE_ROOT=$HOME/nek5_svn/trunk/nek TOOLS_ROOT=$HOME/nek5_svn/trunk/tools EXAMPLES_ROOT=$HOME/nek5_svn/examples python3 nekUnitTests.py
```

#### Standalone

Running the module directly through the interpreter will run all the tests in 
the module.  
`$ python3 nekUnitTests.py`

#### nose

A third-party tool, such as "nose", allows you to run all or a subset of tests.  To run all the tests,
```
$ nosetests nekUnitTests.py
```
To run all the tests for a class, use a command such as:
```
$ nosetests nekUnitTests.py:TurbChannelPnPn
```
To run one test for a givne class, use a command such as:
```
$ nosetests nekUnitTests.py:TurbChannelPnPn.test_GmresSerial
```

Legacy Buildbot Tests
---------------------

### To Run Buildbot Manually On Any Platform(with at least 4 processors)
1.  Make sure you have a current set of the examples from the repo
    in your nek5_svn/examples directoy. (And your nek5_svn/tests directory
    is up to date as well)

2. `$ cd nek5_svn/tests`

3. `$ cp BB_RunTest your_RunTest`
   Edit your_RunTest with the compilers, MOAB directories, Matlab executable path
   that you want to test.  The current BB_RunTest is set to test 3 compilers, 
   one MPI implementation, along with the MOAB and AMG(matlab) tests.

   To run the Analysis step within the you_RunTest (as opposed to running it later, 
   separately, in step 5), include the commented out line:
  
      ./Analysis.py ${PERFORMED_TESTS} &> Analysis.log
  
   Remember to add a 
      mv Analysis.log ./$COMPILER
   to your script to move this log to the directoy of your test results.

   Note -- to disable any test, leave that parameter empty.  For example, 
   to NOT run a parallel compiler test:
   F77_MPI=''
   CC_MPI=''

 
4. `$ your_RunTest`
   This will execute the testing sequence.  

5. To Analyze the test results run `Analysis.py ifmpi` in the directory
   created for the compiler you are testing.  `ifmpi` is a string 
   to trigger if MPI tests are to be analyzed.  Analysis.py mpi will 
   run MPI analysis, and Analysis.py serial will run serial only 
   analysis.

The logfiles from each run will be placed in a sub-directory under 
nek5_svn/tests.  These directories are named according to the compiler
used in the test.  This parameter should be set in the your_RunTest
script.  If this is not the 
first time you have ran the Buildbot tests, you may want to move 
or delete previous logfiles to prevent false positives in the Analysis.

Analysis.py is the script that will actually run the analysis on the 
tests done in RunTests.  An ' F ' is shown for tests that have failed.

A quick way to check what tests failed is to:
   `$ Analysis.py mpi | grep ' F '`


### Overview of the Buildbot Scripts


#### RunTests:
RunTests is the main driver of the buildbot tests.  This script compiles
the nek tools, edits SIZE and .rea files, and calls ExTest and ExTestmpi

For all examples, the .map files are removed and generated from the 
Nek5000 tool, genmap. 

#### ExTestmpi:
This is the script that RunTests calls that has the set of parallel
tests for each example using the parallel compiler provided by the
F77_MPI and CC_MPI parameters.

#### ExTest:  
This is the script RunTests calls that has the set of serial tests for
each example using the compiler set by F77_SRL and CC_SRL parameters.

#### Analysis.py ifmpi	
Python script used to analyze the results of RunTests:
        -takes a string as a parameter to test mpi or not
         If the string is == "mpi" mpi analysis will be ran
         Otherwise, it will not.

	-Tests for successful 'tools' compilation
	-Tests Serial time elapsed 
	-Tests for Serial and Parallel error checks
	-Tests Examples for iteration counts in pressure solver

Legacy Jenkins Tests
--------------------

These scripts perform the same analyses as the BuildBot scripts.  Unlke the
BuildBot scripts, they utilizes testing frameworks from the 'unittest' Python
standard library module.  Additionally, they can produce xUnit-compatable XML
reports by using the 'xmlrunner' module from the Python Package Index. 

Unless you want xUnit XML output, the Buildbot scripts are generally easier to
use.  

### To Run Jenkins Manually On Any Platform(with at least 4 processors)

1.  Make sure you have a current set of the examples from the repo
    in your nek5_svn/examples directoy. (And your nek5_svn/tests directory
    is up to date as well)

2. `$ cd nek5_svn/tests`

3. `$ cp Jenkins_RunTest your_RunTest`
   Edit your_RunTest with the compilers, MOAB directories, Matlab executable path
   that you want to test.  Jenkins_RunTest is currently configured to use one
   of three compilers, one MPI implementation, along with the MOAB and
   AMG(matlab) tests.

4. `$ export COMPILER=[PGI|GNU|INTEL]`
   `$ ./Jenkins_RunTest`
   This will execute the testing sequence for the specified compiler.  

5. `$ cd $COMPILER`
   `$ ../Jenkins_Analysis.py [mpi] [xml] > Analysis.log 2> Analysis.stderr`

  The optional 'mpi' argument will analyze MPI tests.  By default, MPI tests
  are not analyzed.

  The optional 'xml' argument will output xUnit-compabtable XML reports to the
  test-reports/ subdirectory.  This functionaly requires the 'xmlrunner' module.
  By default, XML reports are not produced.  

  The results are in the two logfiles.  


### Overview of the Buildbot Scripts

#### Jenkins_RunTest:
This executes RunTests for a single compiler (PGI, GNU, or Intel).  The
compiler is specified by the COMPILER environment variable.  

#### Jenkins_Analysis.py:
This script performs the same analyses as Analysis.py.  Its stdout is almost
identical to the output from Analysis.py and can be interpreted similarly.  For
example, a quick way to check what tests failed is:

   `Analysis.py mpi | grep ' F '`

The script's stderr is produced by the unittest framework and contains detailed
backtrace information for failed tests. 

The console output is easier to interpret if stdout and stderr are
redirected to separate destinations.  For example:

  `Jenkins_Analysis.py [mpi] [xml] > Analysis.log 2> Analysis.stderr`

which will redirect stdout and stderr to Analysis.log and Analysis.stderr
respectively.
