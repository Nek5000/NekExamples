import unittest

from tools.nekBinBuild import build_tools, build_nek
from tools.nekBinRun import *
from tools.nekFileConfig import config_size

###############################################################################
#  DECORATORS
###############################################################################

def pn_pn_testcase(cls, serial_log_suffix='.pn_pn.serial', parallel_log_suffix='.pn_pn.parallel'):
    """  Decorator to set log suffixes """
    cls.serial_log_suffix   = serial_log_suffix
    cls.parallel_log_suffix = parallel_log_suffix
    return cls

def pn_pn_2_testcase(cls, serial_log_suffix = '.pn_pn_2.serial', parallel_log_suffix='.pn_pn_2.parallel'):
    """  Decorator to set sets log suffixes """
    cls.serial_log_suffix   = serial_log_suffix
    cls.parallel_log_suffix = parallel_log_suffix
    return cls

def serial_test(method):
    """ A decorator for use with NekTestCase methods. Sets logfiles. """
    def wrapper(self, *args):
        cls = self.__class__
        if cls.ifmpi:
            suffix = cls.parallel_log_suffix
        else:
            suffix = cls.serial_log_suffix
        self.logfile = os.path.join(
            cls.examples_root,
            cls.example_subdir,
            "{0}.log.1{1}".format(cls.rea_file, suffix)
        )
        method(self, *args)
    return wrapper

def parallel_test(method):
    """ A decorator for use with NekTestCase methods. Sets logfiles and skips if mpi is disabled """
    def wrapper(self, *args):
        cls = self.__class__
        if not cls.ifmpi:
            self.skipTest("Skipping \"{0}\"; MPI is not enabled.".format(self.id()))
        else:
            self.logfile = os.path.join(
                cls.examples_root,
                cls.example_subdir,
                "{0}.log.4{1}".format(cls.rea_file, cls.parallel_log_suffix)
            )
            method(self, *args)
    return wrapper

###############################################################################
#  BASE TEST CASE
###############################################################################

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

    # Must be defined in setUpClass
    makenek       = ""
    tools_bin     = ""

    # Optionally redefined in subclasses
    log_root       = ""

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
        cls.log_root      = os.environ.get('LOG_ROOT',      cls.log_root)
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
        for val, name in ((cls.tools_bin, 'TOOLS_BIN'),
                          (cls.log_root,  'LOG_ROOT')):
            if val:
                if os.path.isdir(val):
                    print('    Using {0} at "{1}"'.format(name, val))
                else:
                    print('    The {0} directory, "{1}" does not exist.  It will be created'.format(name, val))
                    os.makedirs(val)

        print("Finished getting setup options!")

    @classmethod
    def setUpClass(cls):

        # TODO: Remove old logs

        cls.get_opts()

        build_tools(
            targets    = ('clean', 'genmap'),
            tools_root = cls.tools_root,
            tools_bin  = cls.tools_bin,
            f77        = 'gfortran',
            cc         = 'gcc',
            bigmem     = 'false'
        )
        config_size(
            infile  = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            outfile = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            lx2 = cls.lx2,
            ly2 = cls.ly2,
            lz2 = cls.lz2
        )
        run_meshgen(
            command = os.path.join(cls.tools_bin, 'genmap'),
            stdin   = [cls.rea_file, '0.5'],
            cwd     = os.path.join(cls.examples_root, cls.example_subdir),
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

    @classmethod
    def tearDownClass(cls):
        if cls.log_root:

            if not os.path.isdir(os.path.join(cls.log_root, cls.example_subdir)):
                os.makedirs(os.path.join(cls.log_root, cls.example_subdir))

            for f in os.listdir(os.path.join(cls.examples_root, cls.example_subdir)):
                if f == 'compiler.out' or f == 'genmap.out' or 'log' in f:
                    os.replace(
                        os.path.join(cls.examples_root, cls.example_subdir, f),
                        os.path.join(cls.log_root, cls.example_subdir, f)
                    )


    def get_value(self, label, column, line=0):
        # Get all lines with label
        with open(self.logfile, 'r') as f:
            line_list = [l for l in f if label in l]
        if not line_list:
            raise ValueError("Could not find label \"{0}\" in logfile \"{0}\".  The run may have failed.".format(
                label, self.logfile))
        try:
            value = float(line_list[line].split()[column])
        except ValueError:
            raise ValueError("Attempted to parse non-numerical value in logfile, \"{0}\".  The logfile may be malformatted".format(self.logfile))
        except IndexError:
            raise IndexError("Fewer lines/columns than expected in logfile, \"{0}\".  Logfile may be malformmated.".format(self.logfile))
        else:
            return value

    def get_phrase(self, label):
        with open(self.logfile, 'r') as f:
            for line in f:
                if label in line:
                    return line
        return None

###############################################################################
#  turbChannel: turbChannel.rea
###############################################################################

class TurbChannel(NekTestCase):
    example_subdir  = 'turbChannel'
    rea_file        = 'turbChannel'
    serial_script   = 'nek10s'
    parallel_script = 'nek10steps'

###############################################################################
#  2d_eigtest: eig1.rea
###############################################################################

# TODO: implement 2d_eigtest

###############################################################################
#  3dbox: b3d.rea
###############################################################################

class ThreeDBox(NekTestCase):

    example_subdir  = '3dbox'
    rea_file        = 'b3d'
    box_file        = 'b3d'
    serial_script   = 'nek10s'
    parallel_script = 'nek10steps'

    @classmethod
    def setUpClass(cls):

        cls.get_opts()

        build_tools(
            targets    = ('clean', 'genbox', 'genmap'),
            tools_root = cls.tools_root,
            tools_bin  = cls.tools_bin,
            f77        = 'gfortran',
            cc         = 'gcc',
            bigmem     = 'false'
        )
        config_size(
            infile  = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            outfile = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            lx2 = cls.lx2,
            ly2 = cls.ly2,
            lz2 = cls.lz2
        )
        run_meshgen(
            command = os.path.join(cls.tools_bin, 'genbox'),
            stdin   = ['b3d.box'],
            cwd     = os.path.join(cls.examples_root, cls.example_subdir),
        )
        mvn(
            src_prefix = 'box',
            dst_prefix = 'b3d',
            cwd = os.path.join(cls.examples_root, cls.example_subdir)
        )
        run_meshgen(
            command = os.path.join(cls.tools_bin, 'genmap'),
            stdin   = [cls.rea_file, '0.5'],
            cwd     = os.path.join(cls.examples_root, cls.example_subdir),
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

###############################################################################
#  axi: axi.rea
###############################################################################

class Axi(NekTestCase):

    example_subdir  = 'axi'
    rea_file        = 'axi'
    serial_script   = 'nekbb'
    parallel_script = 'neklmpi'

    @classmethod
    def setUpClass(cls):

        cls.get_opts()

        build_tools(
            targets    = ('clean', 'genbox', 'genmap'),
            tools_root = cls.tools_root,
            tools_bin  = cls.tools_bin,
            f77        = 'gfortran',
            cc         = 'gcc',
            bigmem     = 'false'
        )
        config_size(
            infile  = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            outfile = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            lx2 = cls.lx2,
            ly2 = cls.ly2,
            lz2 = cls.lz2
        )
        run_meshgen(
            command = os.path.join(cls.tools_bin, 'genbox'),
            stdin   = ['axi.box'],
            cwd     = os.path.join(cls.examples_root, cls.example_subdir),
            )
        run_meshgen(
            command = os.path.join(cls.tools_bin, 'genmap'),
            stdin   = ['box', '0.2'],
            cwd     = os.path.join(cls.examples_root, cls.example_subdir),
            )
        mvn(
            src_prefix = 'box',
            dst_prefix = 'axi',
            cwd = os.path.join(cls.examples_root, cls.example_subdir)
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

####################################################################
#  benard: ray_9.rea, ray_dd.rea, ray_dn.rea, ray_nn.rea
####################################################################

# TODO: implement benard

####################################################################
#  blasius: blasius.rea
####################################################################

class Blasius(NekTestCase):
    example_subdir  = 'blasius'
    rea_file        = 'blasius'
    serial_script   = 'nek10s'
    parallel_script = 'nek10steps'

####################################################################
#  cone: cone.rea, cone016.rea, cone064.rea, cone256.rea
####################################################################

# TODO: implement cone

####################################################################
#  conj_ht: conj_ht.rea
####################################################################

class ConjHt(NekTestCase):
    example_subdir  = 'conj_ht'
    rea_file        = 'conj_ht'
    serial_script   = 'nekbb'
    parallel_script = 'neklmpi'

####################################################################
#  cyl_restart: ca.rea, cb.rea, pa.rea, pb.rea
####################################################################

class CylRestart(NekTestCase):
    # No rea_file here; defined in subclasses below
    example_subdir  = 'cyl_restart'
    serial_script   = 'nekbb'
    parallel_script = 'neklmpi'

class CylRestartCa(CylRestart):
    rea_file = 'ca'

class CylRestartCb(CylRestart):
    rea_file = 'cb'

class CylRestartPa(CylRestart):
    rea_file = 'pa'

class CylRestartPb(CylRestart):
    rea_file = 'pb'

####################################################################
#  eddy; eddy_uv.rea, amg_eddy.rea, htps_ed.rea
####################################################################

# TODO: implement eddy for amg_eddy.rea, htps_ed.rea

class EddyEddyUv(NekTestCase):

    example_subdir  = 'eddy'
    rea_file        = 'eddy_uv'
    serial_script   = 'nekbb'
    parallel_script = 'neklmpi'

    @classmethod
    def setUpClass(cls):
        from re import sub

        cls.get_opts()

        build_tools(
            targets    = ('clean', 'genmap'),
            tools_root = cls.tools_root,
            tools_bin  = cls.tools_bin,
            f77='gfortran',

            cc         = 'gcc',
            bigmem     = 'false'
        )
        config_size(
            infile  = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            outfile = os.path.join(cls.examples_root, cls.example_subdir, 'SIZE'),
            lx2 = cls.lx2,
            ly2 = cls.ly2,
            lz2 = cls.lz2
        )

        # Tweak .rea
        rea_path = os.path.join(cls.examples_root, cls.example_subdir, cls.rea_file+'.rea')
        with open(rea_path, 'r') as f:
            lines = [sub(r'^.*DIVERGENCE$', '      0.10000E-08', l) for l in f]
        with open(rea_path, 'w') as f:
            f.writelines(lines)

        run_meshgen(
            command = os.path.join(cls.tools_bin, 'genmap'),
            stdin   = [cls.rea_file, '0.5'],
            cwd     = os.path.join(cls.examples_root, cls.example_subdir),
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
