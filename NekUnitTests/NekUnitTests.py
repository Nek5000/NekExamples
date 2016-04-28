import unittest
import subprocess
import fileinput
import os
import stat
import re

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
    makenek        = ""
    tools_bin      = ""

    # Defined in subclasses only; included here to make syntax checker happy
    example_subdir = ""
    rea_file       = ""
    size_file      = ""

    @classmethod
    def build_tools(cls):
        """ Builds the Nek tools (genmap, prenek, etc) after some tweaks to maketools and prenek/basics.inc

            Sets nelem=10 0000 in prenek/basics.inc

            Side-effects:
                Replaces maketools (backs it up in maketools.bak)
                Replaces prenek/basics.inc (backs it up in prenek/basics.inc.bak)
        """
        print('Compiling tools in {0}... '.format(cls.tools_root))
        print('    using "{0}" as F77'.format(cls.f77))
        print('    using "{0}" as CC'.format(cls.cc))

        maketools          = os.path.join(cls.tools_root, 'maketools')
        basics_inc         = os.path.join(cls.tools_root, 'prenek', 'basics.inc')

        try:
            with fileinput.input(maketools, inplace=True, backup='.bak') as f:
                for line in f:
                    line = re.sub(r'^F77=\"+.+?\"+',   r'F77="{0}"'.format(cls.f77), line)
                    line = re.sub(r'^CC=\"+.+?\"+',    r'CC="{0}"'.format(cls.cc), line)
                    line = re.sub(r'BIGMEM=\"+.+?\"+', r'BIGMEM="false"', line)
                    print(line.rstrip())
            os.chmod(maketools,
                    stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH |
                    stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH |
                    stat.S_IWUSR )

            with fileinput.input(basics_inc, inplace=True, backup='.bak') as f:
                for line in f:
                    line = re.sub(r'(.*nelm *= *)[ 0-9]+(.*)', r'\g<1>10 000\g<2>', line)
                    print(line.rstrip())

            # TODO: turn 'maketools clean' back on
            #subprocess.check_call([maketools, 'clean', cls.tools_bin], cwd=cls.tools_root)
            subprocess.check_call([maketools, 'all',   cls.tools_bin], cwd=cls.tools_root)

        except:
            print('Could not compile tools!')
            raise
        else:
            print('Successfully compiled tools!')

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

        print("Finished getting setup options!")

        # Build tools
        cls.build_tools()

        # Tweak makenek
        print('Setting SOURCE_ROOT, F77, CC, IFMPI in "{0}"...'.format(cls.makenek))
        with fileinput.input(cls.makenek, inplace=True, backup='.bak') as f:
            for line in f:
                line = re.sub(r'^SOURCE_ROOT=\"+.+?\"+', r'SOURCE_ROOT="{0}"'.format(cls.source_root), line)
                line = re.sub(r'^F77=\"+.+?\"+', r'F77="{0}"'.format(cls.f77), line)
                line = re.sub(r'^CC=\"+.+?\"+', r'CC="{0}"'.format(cls.cc), line)
                line = re.sub(r'^#*IFMPI=\"+.+?\"+', r'IFMPI="{0}"'.format(
                    str(cls.ifmpi).lower()), line)
                print(line.rstrip())
        os.chmod(cls.makenek,
                 stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH |
                 stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH |
                 stat.S_IWUSR )


    @classmethod
    def tearDownClass(cls):
        """ A stub for tear-down class.  Might move logs? """
        # TODO: move logs
        pass

    @classmethod
    def run_genmap(cls, tolerance=".05"):
        """ Runs genmap, using the .rea file defined by cls.rea_file

            Not useful in base class.  Useful in subclass for a given example,
            where cls.rea_file is defined

        Params:
            tolerance (str): Mesh tolerance.
                             It's a string, not a float, since it's piped into stdin as a literal
        """
        print("Running genmap...")
        try:
            subprocess.Popen([os.path.join(cls.tools_bin, 'genmap')],
                             stdin=subprocess.PIPE,
                             cwd=os.path.join(cls.examples_root, cls.example_subdir)
            ).communicate(bytes("{0}\n{1}".format(cls.rea_file, tolerance), 'ascii'))
        except:
            print("Could not complete genmap!")
            raise
        print("Succefully finished genmap!")

    @classmethod
    def run_makenek(cls, target=None):
        """ Runs makenek, using the examples subdirectory as the current working directory

            Not useful in base class.  Useful in subclass for a given example.

        Params:
            target (str): target for makenek, e.g. clean, rea [default: cls.rea_file]
        """
        # Can't use default argument since cls is not defined
        if not target:
            target = cls.rea_file
        subprocess.check_call([cls.makenek, target, cls.source_root],
                              cwd=os.path.join(cls.examples_root, cls.example_subdir))

    @classmethod
    def run_nek10s(cls, log_suffix=".log.1"):
        """ Emulates the 'nek10s' script to run nek5000.

            Not useful in base class.  Useful in subclass for a given example.

            Params:
                log_suffix (str): Suffix for logfile [default: '.log.1']
        """

        example_cwd = os.path.join(cls.examples_root, cls.example_subdir)

        session_name =  os.path.join(example_cwd, "SESSION_NAME")
        with open(session_name, "w") as f:
            f.write(cls.rea_file)
            f.write(example_cwd)

        ioinfo = os.path.join(example_cwd, "ioinfo")
        with open(ioinfo, "w") as f:
            f.write("-10")

        nek5000 = os.path.join(example_cwd, "nek5000")
        logfile = os.path.join(example_cwd, "{0}{1}".format(cls.rea_file, log_suffix))
        with open(logfile, 'w') as f:
            subprocess.check_call([nek5000], cwd=example_cwd,  stdout=f)


class PnPnTestCase(NekTestCase):
    """ Base class for Pn-Pn test cases.  Tweaks size file after doing everything in NekTestCase. """

    @classmethod
    def setUpClass(cls):
        """ Tweaks SIZE file for Pn-Pn problems.

            Sets lx2=lx1, ly2=ly1, and lz2=lz1 in SIZE.  Also tweaks makenek, maketools, and
            run maketools (see NekTestCase.setUpClass).
        """

        super(PnPnTestCase, cls).setUpClass()

        # Tweak SIZE file
        size_file_path = os.path.join(cls.examples_root, cls.example_subdir, cls.size_file)
        print('Setting parmeters in "{0}"...'.format(size_file_path))
        with fileinput.input(size_file_path, inplace=True, backup='.bak') as f:
            for line in f:
                # Set lx2=lx1, ly2=ly1, and lz2=lz1
                line = re.sub(r'^ {6}parameter *\( *l([xyz])2 *= *\S+? *\)',
                              r'      parameter (l\g<1>2=l\g<1>1)',
                              line)
                print(line.rstrip())

class PnPn2TestCase(NekTestCase):
    """ Base class for Pn-Pn-2 test cases.  Tweaks size file after doing everything in NekTestCase """

    @classmethod
    def setUpClass(cls):
        """ Tweaks SIZE file for Pn-Pn-2 problems.

            Sets lx2=lx1-2, ly2=ly1-2, and lz2=lz1 in SIZE.  Also tweaks makenek, maketools, and
            run maketools (see NekTestCase.setUpClass).
        """

        super(PnPn2TestCase, cls).setUpClass()

        # Tweak SIZE file
        size_file_path = os.path.join(cls.examples_root, cls.example_subdir, cls.size_file)
        print('Setting parmeters in "{0}"...'.format(size_file_path))
        with fileinput.input(size_file_path, inplace=True, backup='.bak') as f:
            for line in f:
                # Set lx2=lx1-2, ly2=ly1-2
                line = re.sub(r'^ {6}parameter *\( *l([xy])2 *= *\S+? *\)',
                              r'      parameter (l\g<1>2=l\g<1>1-2)',
                              line)
                # Subst lz2=lz1.  Some subclasses will set lz2=lz1-2
                line = re.sub(r'^ {6}parameter *\( *lz2 *= *\S+? *\)',
                              r'      parameter (lz2=lz1)',
                              line)
                print(line.rstrip())

class TurbChannelPnPn(PnPnTestCase):
    """ Test case for turbChannel Pn-Pn examples

        Class attributes:
            example_subdir (str):    Subdirectory for turbChannel [default: 'turbChannel']
            rea_file (str):          [default: 'turbChannel']
            size_file (str):         [default: 'SIZE']
            serial_log_suffix (str): [default '.log.serial']
    """
    example_subdir = "turbChannel"
    rea_file       = 'turbChannel'
    size_file      = 'SIZE'

    serial_log_suffix  = ".log.serial"
    #mpi_log_suffixes   = {1:"log.mpi.1", 4:"log.mpi.4"}

    @classmethod
    def setUpClass(cls):
        """ Runs genmap and builds/runs nek5000 for both serial and (if requested) parallel runs.

            Emulates 'nek10s' script for serial runs.  Emulates 'nek10steps' script for parallel runs.
        """
        super(TurbChannelPnPn, cls).setUpClass()

        cls.run_genmap()
        # TODO: turn 'makenek clean' back on
        #cls.run_makenek('clean')
        cls.run_makenek(cls.rea_file)

        if not cls.ifmpi:
            cls.run_nek10s(log_suffix=cls.serial_log_suffix)
        else:
            #cls.run_nek10steps()
            #cls.run_nek10steps()
            pass


    def test_GmresSerial(self):
        """ Greps gmres from setUpClass to find/compare test values """
        label     = 'gmres:'  # Greps for line with this label
        column    = 7         # Looks in this column for test value (counted from RIGHT)
        target_value = 0.     # Target gmres value
        delta = 95.       # Success if test value is within target_value +/- delta
        cls = self.__class__

        logfile = os.path.join(cls.examples_root, cls.example_subdir,
                               "{0}{1}".format(cls.rea_file, cls.serial_log_suffix))
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
                        print('SUCCESS: test_GmresSerial: {1} was within {2} +/ {3}'.format(
                            test_value, target_value, delta ))
                        break


    def test_GmresParallel(self):
        """ Greps gmres from setUpClass to find/compare test values """
        cls = self.__class__
        if not cls.ifmpi:
            self.skipTest("Skipping \"{0}\"; MPI is not enabled.".format(self.id()))
        else:
            # TODO: implement parallel test
            pass


if __name__ == '__main__':
    unittest.main()
