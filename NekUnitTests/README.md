Nek unittests
=============

The NekUnitTests module contains the Nek5000 verification tests, implmented 
using  the Python standard-library unittests framework.  The modules require 
Python 3.2 or higher.  

Module Contents
---------------

The module contains the following classes and methods (listed as items and 
subitems,  respectively):

* TurbChannelPnPn
  * test_GmresSerial
* TurbChannelPnPn2
  * test_GmresSerial
  
Running Tests
-------------

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
$ SOURCE_ROOT=$HOME/nek5_svn/trunk/nek TOOLS_ROOT=$HOME/nek5_svn/trunk/tools EXAMPLES_ROOT=$HOME/nek5_svn/examples python3 NekUnitTests.py
```

### Standalone

Running the module directly through the interpreter will run all the tests in 
the module.  
`$ python3 NekUnitTests.py`

### nose

A third-party tool, such as "nose", allows you to run all or a subset of tests.  To run all the tests,
```
$ nosetests NekUnitTests.py
```
To run all the tests for a class, use a command such as:
```
$ nosetests NekUnitTests.py:TurbChannelPnPn
```
To run one test for a givne class, use a command such as:
```
$ nosetests NekUnitTests.py:TurbChannelPnPn.test_GmresSerial
```
    

