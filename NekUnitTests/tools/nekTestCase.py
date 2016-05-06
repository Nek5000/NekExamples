import unittest

from tools.nekBinBuild import build_tools, build_nek
from tools.nekBinRun import *
from tools.nekFileConfig import config_size

def skip_unless_mpi(F):
    """ A decorator for use with NekTestCase methods. Skips test if MPI is disabled. """
    def wrapper(instance, *args):
        cls = instance.__class__
        if not cls.ifmpi:
            instance.skipTest("Skipping \"{0}\"; MPI is not enabled.".format(instance.id()))
        else:
            F(instance, *args)
    return wrapper

class NekTestCase(unittest.TestCase):
    """ Base class for Nek unittests

    This defines a setUpClass method to:
        (a) get the relevant environment variables for compilers, directories
        (b) add env vars to maketools, makenek
        (b) build tools
    All subclassed TestCases will need to do these things.

    Class attributes:
        f77 (str):            The Fortran 77 compiler to use     [default: 'gfortran']
        cc (str):             The C compiler to use              [default: 'gcc']
        ifmpi (bool):         Perform compilation/tests with MPI [default: False]
        source_root (str):    Path to Nek source directory;overridden by $SOURCE_ROOT env variable
                              [default: '$HOME/nek5_svn/trunk/nek']
        tools_root (str):     Path to Nek tools directory; overridden by $TOOLS_ROOT env variable
                              [default: '$HOME/nek5_svn/trunk/tools']
        examples_root (str):  Path to Nek examples directory; overridden by $EXAMPLES_ROOT env variable
                              [default: '$HOME/nek5_svn/examples']
        makenek (str):        Path to makenek                    [default: source_root/makenek]
        tools_bin (str):      Directory to place compiled tools  [default: tools_root/bin]

    Subclass attributes:
        These aren't meaningful in the base class.  They're intended for a subclass that represents
        a particular example problem.
        example_subdir (str): The subdirectory for the subclass' example.  Assumed that it's in example_root
        rea_file (str):       The .rea file for the subclass' example, minus the '.rea' extension.  Assumed
                              that it's in example_root/example_dir
        size_file (str):      The SIZE file for the subclass' example.  Assuemed that it's in
                              example_root/example_subdir
    """

    # Default values, can be redefined in setUpClass
    f77            = "gfortran"
    cc             = "gcc"
    ifmpi          = False
    source_root    = "{0}/nek5_svn/trunk/nek".format(os.environ.get('HOME', ""))
    examples_root  = "{0}/nek5_svn/examples".format(os.environ.get('HOME', ""))
    tools_root     = "{0}/nek5_svn/trunk/tools".format(os.environ.get('HOME', ""))
    # TODO: do something productive with tests_root and log_root; right now they're not used
    # tests_root     = "{0}/nek5_svn/tests".format(os.environ.get('HOME', ""))
    # log_root       = os.path.join(tests_root, "logs")

    # Defined in setUpClass
    makenek       = ""
    tools_bin     = ""
    serial_log    = ""
    parallel_logs = {}

    # Optionally redefined in subclasses
    mpi_procs      = ("1", "4")

    # Must be defined in subclasses only; included here to make syntax checker happy
    example_subdir      = ""
    rea_file            = ""
    serial_script       = ""
    serial_log_suffix   = ""
    parallel_script     = ""
    parallel_log_suffix = ""
    lx2 = None
    ly2 = None
    lz2 = None

    @classmethod
    def get_opts(cls):
        # TODO: try to clean up all this mess...

        print("Getting setup options...")

        # Get compilers from env, default to GNU
        cls.f77   = os.environ.get('F77',   cls.f77)
        cls.cc    = os.environ.get('CC',    cls.cc)
        cls.ifmpi = os.environ.get('IFMPI', cls.ifmpi)

        # String/bool conversion
        ifmpi_str = str(cls.ifmpi).lower()
        cls.ifmpi = ifmpi_str == 'yes' or ifmpi_str == 'true'

        for name, val in (('F77', cls.f77),
                          ('CC', cls.cc),
                          ('IFMPI', str(cls.ifmpi).lower())):
            print('    Using {0}="{1}"'.format(name, val))

        # Get Nek5000 dirs from env, if defined
        cls.source_root   = os.environ.get('SOURCE_ROOT',   cls.source_root)
        cls.tools_root    = os.environ.get('TOOLS_ROOT',    cls.tools_root)
        cls.examples_root = os.environ.get('EXAMPLES_ROOT', cls.examples_root)
        #cls.tests_root    = os.environ.get('TESTS_ROOT',    cls.tests_root)
        #cls.log_root      = os.environ.get('LOG_ROOT',      cls.log_root)
        if not cls.makenek:
            cls.makenek   = os.path.join(cls.source_root, 'makenek')
        if not cls.tools_bin:
            cls.tools_bin = os.path.join(cls.tools_root, 'bin')

        # Raise error if source_, tools_, tests_, examples_root don't exist
        for val, name in ((cls.source_root,   'SOURCE_ROOT'),
                          #(cls.tests_root,    'TESTS_ROOT'),
                          (cls.examples_root, 'EXAMPLES_ROOT'),
                          (cls.tools_root,    'TOOLS_ROOT')):
            if os.path.isdir(val):
                print('    Using {0} at "{1}"'.format(name, val))
            else:
                raise RuntimeError('The {0} directory, "{1}", does not exist. \
                Please set ${0} to a valid path.'.format(name, val))

        # Make tools_bin if it doesn't exist
        if not os.path.isdir(cls.tools_bin):
            print('    The directory "{0}" does not exist.  It will be created'.format(cls.tools_bin))
            os.makedirs(cls.tools_bin)

        # Make log_root if it doesn't exist
        # if os.path.isdir(cls.log_root):
        #     print('    Using LOG_ROOT at "{0}"'.format(cls.log_root))
        # else:
        #     print('    The LOG_ROOT, "{0}", does not exist.  It will be created.'.format(cls.log_root))
        #     os.makedirs(cls.log_root)

        # Set log names
        cls.serial_log = os.path.join(cls.examples_root, cls.example_subdir,
                                      "{0}.log.1{1}".format(cls.rea_file, cls.serial_log_suffix))
        cls.parallel_logs = {p: os.path.join(cls.examples_root, cls.example_subdir,
                                             "{0}.log.{1}{2}".format(cls.rea_file, p, cls.parallel_log_suffix))
                             for p in cls.mpi_procs}

        print("Finished getting setup options!")

    @classmethod
    def setUpClass(cls):
        """ Set up for subsequent unit tests

        Does the following
            (a) get the relevant environment variables for compilers, directories
            (b) sets the following class attributes:
                f77
                cc
                ifmpi
                source_root
                tools_root
                examples_root
                makenek
                tools_bin
            (c) add f77, cc, ifmpi and source_root to maketools, makenek
            (d) build tools

        Side-effects:
            Replaces makenek (backs it up in makenek.bak)
            Replaces maketools (backs it up in maketools.bak)
            Replaces prenek/basics.inc (backs it up in prenek/basics.inc.bak)
        """

        # Get user options
        cls.get_opts()

        build_tools(
            targets    = ('clean', 'genmap'),
            tools_root = cls.tools_root,
            tools_bin  = cls.tools_bin,
            f77        = 'gfortran',
            cc         = 'gcc',
            bigmem     = 'false'
        )

        run_genmap(
            tools_bin = cls.tools_bin,
            rea_file  = cls.rea_file,
            cwd       = os.path.join(cls.examples_root, cls.example_subdir),
            tolerance = '.05'
        )

        config_size(
            infile  = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            outfile = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            lx2 = cls.lx2,
            ly2 = cls.ly2,
            lz2 = cls.lz2
        )

        build_nek(
            source_root = cls.source_root,
            rea_file    = cls.rea_file,
            cwd         = os.path.join(cls.examples_root, cls.example_subdir),
            f77         = cls.f77,
            cc          = cls.cc,
            ifmpi       = str(cls.ifmpi).lower()
        )

        # Serial run
        if not cls.ifmpi:
            run_nek_script(
                script     = os.path.join(cls.tools_root, 'scripts', cls.serial_script),
                rea_file   = cls.rea_file,
                cwd        = os.path.join(cls.examples_root, cls.example_subdir),
                log_suffix = cls.serial_log_suffix
            )
        # Parallel run
        else:
            run_nek_script(
                script     = os.path.join(cls.tools_root, 'scripts', cls.parallel_script),
                rea_file   = cls.rea_file,
                cwd        = os.path.join(cls.examples_root, cls.example_subdir),
                log_suffix = cls.parallel_log_suffix,
                mpi_procs  = ("1", "4")
            )

    def check_value(self, logfile, label, column, target_value, delta):

        with open(logfile, 'r') as f:
            for line in f:
                if label in line:
                    try:
                        test_value = float(line.split()[-column])
                    except ValueError:
                        raise ValueError("Attempted to parse non-numerical value in logfile, \"{0}\".  The logfile may be malformatted".format(logfile))
                    except IndexError:
                        raise IndexError("Fewer columns than expected in logfile, \"{0}\".  Logfile may be malformmated.".format(logfile))
                    else:
                        self.assertAlmostEqual(test_value, target_value, delta=delta)
                        # TODO: Figure out how to print successes; this doesn't work with unittest.main()
                        # print('SUCCESS: {1} was within {2} +/ {3}'.format( test_value, target_value, delta ))
                        return
        self.fail('Could not find the label, "{0}", in the logfile, "{1}".'.format(label, logfile))
